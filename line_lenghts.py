import bold
from collections import defaultdict

def get_line_lengths(lines, print_values=False, bold_lines = False):
    whitespace_to_lines = defaultdict(lambda:[])
    for line in lines:
        if bold_lines:
            if not bold.line_bold_checks(line):
                continue
            line = bold.remove_bold_tags(line)
        whitespace_length = get_preceding_whitespace_length(line)
        whitespace_to_lines[whitespace_length].append(line)
    if print_values:
        print_line_lengths(whitespace_to_lines)
    return whitespace_to_lines


# def get_bold_lengths(lines, print_values=False):
#     whitespace_to_lines = defaultdict(lambda:[])
#     for line in lines:
#         if not bold.line_bold_checks(line):
#             continue
#         line = bold.remove_bold_tags(line)
#         whitespace_length = get_preceding_whitespace_length(line)
#         whitespace_to_lines[whitespace_length].append(line)
#     if print_values:  
#         print_line_lengths(whitespace_to_lines) 
#     return whitespace_to_lines


def print_line_lengths(whitespace_to_lines):
    for key in whitespace_to_lines:
            for ex in whitespace_to_lines[key][:2]:
                print(key,end=':  ')
                print(ex)


def get_preceding_whitespace_length(line):
    return len(line)-len(line.lstrip(' '))

