import re


def find_operators(file_path):
    excluded_operators = set(['<<', '>>', '//', '/*', '*/'])
    operators = r'[-+*/%=<>!&|^?~]+'
    operator_pattern = re.compile(operators)

    with open(file_path, 'r') as file:
        lines = file.readlines()

    operator_info = []

    for line_index, line in enumerate(lines):
        if '#include' in line:
            continue
        matches = operator_pattern.finditer(line)
        for match in matches:
            start_index, end_index = match.span()
            operator_value = match.group(0)

            if operator_value not in excluded_operators:
                operator_info.append({
                    'line_index': line_index,
                    'start_index': start_index,
                    'end_index': end_index,
                    'operator': operator_value
                })

    return operator_info


def find_break_and_continue(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    break_and_continue_info = []

    for line_index, line in enumerate(lines):
        if '#include' in line:
            continue
        line = line.strip()
        if line.startswith('break'):
            start_index = line.find('break')
            end_index = start_index + len('break')
            break_and_continue_info.append({
                'line_index': line_index,
                'start_index': start_index,
                'end_index': end_index,
                'statement': 'break'
            })
        elif line.startswith('continue'):
            start_index = line.find('continue')
            end_index = start_index + len('continue')
            break_and_continue_info.append({
                'line_index': line_index,
                'start_index': start_index,
                'end_index': end_index,
                'statement': 'continue'
            })

    return break_and_continue_info


def find_numbers(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    number_info = []

    for line_index, line in enumerate(lines):
        if '#include' in line:
            continue
        matches = re.finditer(r'\b(\d+(\.\d+)?)\b', line)

        for match in matches:
            start_index, end_index = match.span()
            number_value = match.group(1)

            number_type = "integer" if '.' not in number_value else "float"

            number_info.append({
                'line_index': line_index,
                'start_index': start_index,
                'end_index': end_index,
                'number': float(number_value) if number_type == "float" else int(number_value),
                'type': number_type
            })

    return number_info

def find_true_false(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    true_false_info = []

    for line_index, line in enumerate(lines):
        if '#include' in line:
            continue
        matches = re.finditer(r'\b(true|false)\b', line)

        for match in matches:
            start_index, end_index = match.span()
            statement_value = match.group(1)

            true_false_info.append({
                'line_index': line_index,
                'start_index': start_index,
                'end_index': end_index,
                'statement': statement_value
            })

    return true_false_info

def find_type_specifiers(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    type_specifier_info = []

    for line_index, line in enumerate(lines):
        if '#include' in line:
            continue
        matches = re.finditer(r'\b(?:int|char|float|double|long|short|signed|unsigned|void|bool|wchar_t|string)\s*(?:\*+\s*)*\b', line)

        for match in matches:
            start_index, end_index = match.span()
            specifier_value = match.group(0)

            type_specifier_info.append({
                'line_index': line_index,
                'start_index': start_index,
                'end_index': end_index,
                'specifier': specifier_value
            })

    return type_specifier_info


def find_else_statements(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    else_info = []

    for line_index, line in enumerate(lines):
        if '#include' in line:
            continue
        matches = re.finditer(r'\belse(?:\s+if)?\b', line)

        for match in matches:
            start_index, end_index = match.span()
            else_statement = match.group(0)

            else_info.append({
                'line_index': line_index,
                'start_index': start_index,
                'end_index': end_index,
                'else_statement': else_statement
            })

    return else_info


if __name__ == "__main__":
    file_path = "C:/Users/Admin/CLionProjects/untitled/main.cpp"
    result = find_operators(file_path)

    for operator_info in result:
        print(f"Line {operator_info['line_index'] + 1}, Start Index: {operator_info['start_index']}, "
              f"End Index: {operator_info['end_index']}, Operator: {operator_info['operator']}")

    break_and_continue_info = find_break_and_continue(file_path)

    for info in break_and_continue_info:
        print(
            f"Line {info['line_index'] + 1}, Start Index: {info['start_index']}, End Index: {info['end_index']}, Statement: {info['statement']}")

    number_info = find_numbers(file_path)

    for info in number_info:
        print(f"Line {info['line_index'] + 1}, Start Index: {info['start_index']}, End Index: {info['end_index']}, Number: {info['number']}, Type: {info['type']}")

    true_false_info = find_true_false(file_path)

    for info in true_false_info:
        print(
            f"Line {info['line_index'] + 1}, Start Index: {info['start_index']}, End Index: {info['end_index']}, Statement: {info['statement']}")

    type_specifier_info = find_type_specifiers(file_path)

    for info in type_specifier_info:
        print(
            f"Line {info['line_index'] + 1}, Start Index: {info['start_index']}, End Index: {info['end_index']}, Specifier: {info['specifier']}")

    else_info = find_else_statements(file_path)

    for info in else_info:
        print(
            f"Line {info['line_index'] + 1}, Start Index: {info['start_index']}, End Index: {info['end_index']}, Statement: {info['else_statement']}")
