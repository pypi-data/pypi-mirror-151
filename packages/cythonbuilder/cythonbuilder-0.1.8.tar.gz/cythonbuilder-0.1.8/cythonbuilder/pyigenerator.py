import re


# from cythonbuilder import logger


def read_write_pyx_to_pyi(target_pyx_path: str, target_pyi_path:str):
    """ Reads all content from a pyx file, convers and writes a pyi """

    # 1. Read pyx file
    pyx_lines: [str] = []
    with open(target_pyx_path, 'r') as open_pyx:
        pyx_lines.extend(open_pyx.readlines())

    # 2. Skip empty lines
    pyx_lines = [l.strip("\n") for l in pyx_lines]
    pyx_lines = [l for l in pyx_lines if (len(l) > 0)]

    # 2. Determine file indentation
    all_indentations = [__get_line_indentation_spacecount(line=l) for l in pyx_lines]
    all_indentations = [i for i in all_indentations if (i > 0)]
    spaces_for_one_tab = min(all_indentations)
    # Extra check: test wheter all are divisible by the space_for_one_tab
    for indent in all_indentations:
        if (indent % spaces_for_one_tab != 0):
            raise ValueError(f"Found invalid indentation: {indent} not divisible by {spaces_for_one_tab}")



    # Convert lines to py
    py_lines:[str] = []
    for line_idx in range(len(pyx_lines)):
        # pyx line to filter
        pyx_line = pyx_lines[line_idx]

        # Line details
        cur_line_is_import = line_is_import(line=pyx_line)
        cur_line_is_function = line_is_function(line=pyx_line)
        cur_line_is_class = line_is_class(line=pyx_line)
        cur_line_spaces = __get_line_indentation_spacecount(line=pyx_lines[line_idx])
        cur_line_indentation: int = int(cur_line_spaces / spaces_for_one_tab) if (cur_line_spaces > 0) else cur_line_spaces

        # FILTERING     Skip if indentation > 2. That way we are one indentation deeper than method content
        if (not cur_line_is_import and not cur_line_is_class and not cur_line_is_function):
            continue



        # FILTERING     Skip if previous line is a function def
        if (line_idx > 0):
            pyx_line_prev = pyx_lines[line_idx - 1]
            pyx_line_prev.strip(' ')
            if (line_is_function(line=pyx_line_prev)):
                pyx_line = f"{cur_line_spaces * ' '}..."

        # only keep lines when the next line has a greater indentation
        # if (line_idx == len(pyx_lines) - 1):
        #     print("breaking")
        #     break
        # current_indentation = __get_line_indentation_spacecount(line=pyx_lines[line_idx])
        # nextline_indentation = __get_line_indentation_spacecount(line=pyx_lines[line_idx + 1])
        # if (nextline_indentation <= current_indentation):
        #     continue

        # print('0', pyx_line)
        py_line = pyx_line_to_pyi(line=pyx_line.strip("\n"), spaces_for_one_tab=spaces_for_one_tab)
        if (py_line != None):
            py_lines.append(py_line)



    with open(target_pyi_path, 'w') as pyi_out:
        pyi_out.writelines([f"{line}\n" for line in py_lines])
        # for line in py_lines:
        #     print(line+'\n')
        #     pyi_out.write(line)


def line_is_import(line:str) -> bool:
    """ """
    return line.split(" ")[0] in ['import', 'cimport']
def line_is_class(line:str) -> bool:
    """ """
    return line[-1] == ":" and "class" in line.split(" ")

def line_is_function(line:str) -> bool:
    """ """
    line = line.strip(' ')
    endswith_colon = line[-1] == ':'
    return endswith_colon and not line_is_class(line=line)
def line_is_c_function(line:str) -> bool:
    is_c_function = False
    if (line_is_function(line=line)):
        line_parts_set = set(line.split(" "))
        cfunction_defs = {'cpdef', 'cdef'}
        if (len(line_parts_set.intersection(cfunction_defs)) > 0):
            is_c_function = True
    return is_c_function



def pyx_line_to_pyi(line: str, spaces_for_one_tab: int):
    """ Interprets a line and converts pyx to pyi
        :arg spaces_for_one_tab       how many spaces equals one level of indentation
    """


    # 1. Calculate indentation level
    spacecount = __get_line_indentation_spacecount(line=line)
    indentation:int = int(spacecount / spaces_for_one_tab) if (spacecount > 0) else spacecount

    # 2. Remove unrequired characters
    line = line.strip(' ')

    # 3. Keep only lines that start with def, cpdef or cdef
    begin_words = ['def', 'cdef', 'cpdef', 'class', 'cimport', 'import']
    if not any([line[:len(w)] == w for w in begin_words]):
        return

    # If class is in the line: make sure it adheres to python def
    splitline = line.split(" ")
    if (splitline[1] == 'class'):
        line = " ".join(splitline[1:])
    if (splitline[0] == 'cimport' or splitline[0] == 'import'):
        splitline[0] = 'import'
        line = " ".join(splitline)


    # 4. Start replacing lines
    line_parts = line.split(" ")
    for word in ['cpdef', 'cdef']:
        if word in line_parts:
            word_idx = line_parts.index(word)
            line_parts[word_idx] = 'def'
    line = " ".join(line_parts)


    # 5. Handle function types
    if (line_is_function(line=line)):
        if ('->' in line):
            line = f"{line.split('->')[0].strip()}:"

        array_between_brackets = re.findall('\(.*?\)',line)
        for brackets in array_between_brackets:
            # Remove return type definition
            func_part_one_old = line.replace(f"{brackets}:", "")
            func_part_one_new = " ".join([func_part_one_old.split(" ")[0], func_part_one_old.split(" ")[-1]])
            line = line.replace(func_part_one_old, func_part_one_new)
            for argument in brackets.split(","):

                # Strip away parentheses and spaces
                argument = argument.strip("() ")

                # C types are split like 'int age'
                arg_array = [a for a in argument.split(" ") if (len(a) > 0)]
                if (len(arg_array) <= 1):
                    continue
                var_ctype = arg_array[0].strip(":")
                var_name = arg_array[1].strip(":")
                if (line_is_c_function(line=line)):
                    var_name, var_ctype = var_ctype, var_name
                py_type = convert_type_cy_to_py(cy_type=var_ctype)
                line = line.replace(argument, f'{var_name}:{py_type}')

        spaces = " " * spaces_for_one_tab * (indentation + 1)
        line = line + f"\n{spaces}..."
    return indentation * spaces_for_one_tab * ' ' + line

def convert_type_cy_to_py(cy_type:str):
    """ """
    # todo continue https://stackoverflow.com/questions/55451545/what-are-all-the-types-available-in-cython
    cy_type = cy_type.lower()

    if (cy_type in ['bint', 'bool']):
        return 'bool'
    elif (cy_type in ['char', 'short', 'int', 'long', 'long long']):
        return 'int'
    elif (cy_type in ['float', 'double', 'long double']):
        return 'float'
    elif (cy_type in ['float complex', 'double complex', 'complex']):
        return 'complex'
    elif (cy_type in ['char*', 'std::string', 'str']):
        return 'str'
    # print(f"{indentation * spaces_for_one_tab * ' '}{line}")


def __get_line_indentation_spacecount(line: str) -> int:
    """ How many spaces is the provided line indented? """
    spaces: int = 0
    if (len(line) > 0):
        if (line[0] == ' '):
            for letter_idx in range(len(line)):
                if (line[letter_idx + 1] != ' '):
                    spaces = letter_idx + 1
                    break
    return spaces