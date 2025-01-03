# Software Testing Final Project
import os
import subprocess

from find_mutant import *
from mutate import Mutation

OPERATOR_MAPPINGS = {
    '+': ['-', '*', '/', '%', '&', '|', '^', '<<', '>>', '+=', '++'],
    '-': ['+', '*', '/', '%', '&', '|', '^', '<<', '>>','-=','--'],
    '*': ['/', '%', '+', '-', '&', '|', '^', '<<', '>>','*=' ],
    '/': ['*', '%', '+', '-', '&', '|', '^', '<<', '>>', '/='],
    '%': ['/', '*', '+', '-', '&', '|', '^', '<<', '>>', '%='],
    '==': ['!=', '<', '<=', '>', '>=', '&&', '||'],
    '!=': ['==', '<', '<=', '>', '>=', '&&', '||'],
    '<': ['>', '>=', '<=', '==', '!=', '&&', '||','<<'],
    '<=': ['>', '>=', '<', '==', '!=', '&&', '||'],
    '>': ['<', '<=', '>=', '==', '!=', '&&', '||', '>>'],
    '>=': ['<', '<=', '>', '==', '!=', '&&', '||'],
    '&&': ['||', '==', '!=', '<', '<=', '>', '>=' '&','|'],
    '||': ['&&', '==', '!=', '<', '<=', '>', '>=', '|', '&'],
    '&': ['|', '^', '~', '<<', '>>', '&&', '||'],
    '|': ['&', '^', '~', '<<', '>>', '&&', '||'],
    '^': ['&', '|', '~', '<<', '>>', '&&', '||'],
    '~': ['&', '|', '^', '<<', '>>'],
    '<<': ['>>', '==', '!=', '<'],
    '>>': ['<<', '==', '!=', '<', ],
    '!': ['', '++', '--'],
    '++': ['+', '--','-'],
    '--': ['++', '--','-'],
}

STATEMENT_MAPPINGS = {
    'else if': ["if"],
    'else': ["if (1==0)"],
}
BOOLEAN_MAPPINGS = {
    'true': ["false"],
    'false': ["true"],
}

LOOP_CONTROLS_MAPPINGS = {
    'break': ["", "continue"],
    'continue': ["", "break"],
}

total_compilable_mutants = 0
total_killed_mutants = 0


def mutate_the_code(source_code_path, temporary_dir, start_line, start_index, end_index, replace, replaced_str):
    test_execute_command = "/tmp/test/cmake-gtest-coverage-example/build/tests/poptests"
    m = Mutation(file_path=source_code_path, temp_directory=temporary_dir)
    m.apply_mutation(
        start_line_number=start_line,
        start_index=start_index,
        end_line_number=start_line,
        end_index=end_index,
        replace_with=replace
    )
    is_compilable = m.check_if_compilable(build_dir)

    print(
        f"change '{replaced_str}' to '{x}' in line '{start_line}' from index '{start_index}' to index '{end_index}' "
        f"compile status: {is_compilable}"
    )
    command = f"{test_execute_command}"

    global total_compilable_mutants
    global total_killed_mutants

    if is_compilable:
        total_compilable_mutants += 1
        with open(os.devnull, 'w') as null_file:
            result = subprocess.run(command, shell=True, stdout=null_file, stderr=null_file)

        is_killed = False if result.returncode == 0 else True
        if is_killed:
            total_killed_mutants += 1

    m.undo_mutation()


# these values must be changed
file_path = "/tmp/test/cmake-gtest-coverage-example/vendor/simple_vendor.cpp"
temp_dir = "/tmp/test/software_testing/tmp"
build_dir = "/tmp/test/cmake-gtest-coverage-example/build"

operators = find_operators(file_path)
break_and_continue_info = find_break_and_continue(file_path)
number_info = find_numbers(file_path)
true_false_info = find_true_false(file_path)
# type_specifier_info = find_type_specifiers(file_path)
else_info = find_else_statements(file_path)

for mutant in operators:
    if not mutant['operator'] in OPERATOR_MAPPINGS:
        continue

    for x in OPERATOR_MAPPINGS[mutant['operator']]:
        mutate_the_code(
            file_path, temp_dir, mutant['line_index'], mutant['start_index'], mutant['end_index'], x,
            mutant['operator'],

        )

for mutant in break_and_continue_info:
    if not mutant['statement'] in LOOP_CONTROLS_MAPPINGS:
        continue

    for x in LOOP_CONTROLS_MAPPINGS[mutant['statement']]:
        mutate_the_code(
            file_path, temp_dir, mutant['line_index'], mutant['start_index'], mutant['end_index'], x,
            mutant['statement']
        )

for mutant in number_info:
    mutate_the_code(
        file_path, temp_dir, mutant['line_index'], mutant['start_index'], mutant['end_index'],
        str(mutant['number'] + 1), mutant['number']
    )
    mutate_the_code(
        file_path, temp_dir, mutant['line_index'], mutant['start_index'], mutant['end_index'],
        str(mutant['number'] - 1), mutant['number']
    )

for mutant in true_false_info:
    if not mutant['statement'] in BOOLEAN_MAPPINGS:
        continue

    for x in BOOLEAN_MAPPINGS[mutant['statement']]:
        mutate_the_code(
            file_path, temp_dir, mutant['line_index'], mutant['start_index'], mutant['end_index'], x,
            mutant['statement']
        )

for mutant in else_info:
    if not mutant['else_statement'] in STATEMENT_MAPPINGS:
        continue

    for x in STATEMENT_MAPPINGS[mutant['else_statement']]:
        mutate_the_code(
            file_path, temp_dir, mutant['line_index'], mutant['start_index'], mutant['end_index'], x,
            mutant['else_statement']
        )

print(f"total mutants: {total_compilable_mutants}")
print(f"killed mutants: {total_killed_mutants}")
