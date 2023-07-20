import bold_utils
import line_utils
from collections import defaultdict


def get_line_lengths(lines, print_values=False, bold_lines = False):
    whitespace_to_lines = defaultdict(lambda:[])
    for line in lines:
        if bold_lines:
            if not bold_utils.line_bold_checks(line):
                continue
            line = bold_utils.remove_bold_tags(line)
        whitespace_length = line_utils.get_preceding_whitespace_length(line)
        whitespace_to_lines[whitespace_length].append(line)
    if 0 in whitespace_to_lines:
        del whitespace_to_lines[0]
    if print_values:
        density_dict = print_line_lenght_density(whitespace_to_lines)
        print_line_lengths(whitespace_to_lines, density_dict)
    return whitespace_to_lines


def print_line_lenght_density(whitespace_to_lines):
    total_lines = sum(len(line_list) for line_list in whitespace_to_lines.values())
    density_dict = {key:round(len(whitespace_to_lines[key]),2)/total_lines for key in sorted(whitespace_to_lines.keys()) 
                    if round(len(whitespace_to_lines[key])/total_lines,2) > 0 and len(whitespace_to_lines[key]) > 1}
    for item in density_dict.items():
        print(f"{item[0]}: {item[1]:.2f}")
    return density_dict


def print_line_lengths(whitespace_to_lines, density_dict):
    for key in sorted(whitespace_to_lines):
        if key not in density_dict:
            continue
        for ex in whitespace_to_lines[key][:2]:
            print(key,end=':  ')
            print(ex)



