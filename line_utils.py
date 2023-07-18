def split_to_lines(text):
    lines = []
    for line in text:
        lines.extend(str(line).splitlines())
    return lines

def get_preceding_whitespace_length(line):
    return len(line)-len(line.lstrip(' '))


def remove_parantheses(lines):
    for i,line in enumerate(lines):
        pstart,pend = find_parantheses(line)
        searching_paranthesis = False
        while open_close_parantheses(lines[i]):
            lines[i] = lines[i].replace(lines[i][pstart:pend+1], '')
        if open_parantheses(line):
            searching_paranthesis = True
            lines[i] = line.replace(line[pstart:], '')
        elif close_parantheses(line):
            searching_paranthesis = False
            lines[i] = line.replace(line[:pend+1], '')   
        elif searching_paranthesis:
            lines[i] = ''
    return lines

def find_parantheses(line):
    return line.find('('),line.find(')')

def open_parantheses(line):
    pstart,pend = find_parantheses(line)
    return pstart != -1 and pend == -1

def close_parantheses(line):
    pstart,pend = find_parantheses(line)
    return pstart == -1 and pend != -1

def open_close_parantheses(line):
    pstart,pend = find_parantheses(line)
    return pstart != -1 and pend != -1


