"""
All processes involving getting and processing bold lines in a script.
Bold lines are used for:
Character Names
Locations
Location Descriptions
Scene Numbers
"""


def get_bold_lines(lines):
    bold_lines = []
    for line in lines:
        if not line_bold_checks(line):
            continue
        line = remove_bold_tags(line)
        line = line.strip()
        bold_lines.append(line)
    return bold_lines


def line_bold_checks(line):
    return line and line_is_bold(line) and line.replace(' ','')


def get_preceding_whitespace_length(line):
    return len(line)-len(line.lstrip(' '))


def line_is_bold(line):
    return line[0] == '<'


def remove_bold_tags(line):
    return line.replace('<b>','').replace('</b>','')