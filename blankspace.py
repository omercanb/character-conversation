import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import random

import characters
import bold
import line_lenghts

"""
example urls: 
halloween: https://imsdb.com/scripts/Halloween.html
joker: https://imsdb.com/scripts/Joker.html
"""

transitions = {
    "BACK TO:",
    "CUT TO:",
    "DISSOLVE TO:",
    "FADE OUT:",
    "FADE IN:",
    "FLASH CUT TO:",
    "FREEZE FRAME:",
    "IRIS IN:",
    "IRIS OUT:",
    "MATCH CUT TO:",
    "MATCH DISSOLVE TO:",
    "SMASH CUT TO:",
    "TIME CUT TO:",
    "WIPE TO:",
}

def main():
    
    url = "https://imsdb.com/scripts/Joker.html"
    soup = get_soup(url)
    text = get_raw_text(soup)
    lines = split_to_lines(text)
    lines = remove_parantheses(lines)
    character_names = characters.get_characters(bold.get_bold_lines(lines), mention_number = 20)
    dialogue = get_dialogue(lines, character_names, dialogue_range = (10,18))
    dialogue_dict = get_dialoague_dict(dialogue, character_names)


def get_dialoague_dict(dialogue, characters):
    dialogue_dict = defaultdict(lambda:[])
    current_character = dialogue[0]
    for line in dialogue:
        if line in characters:
            current_character = line
            continue
        dialogue_dict[current_character].append(line.strip())
    return dialogue_dict



def remove_parantheses(lines):
    for i,line in enumerate(lines):
        pstart = line.find('(')
        pend = line.find(')')
        while pstart != -1 and pend != -1:
            lines[i] = lines[i].replace(lines[i][pstart:pend+1], '')
            pstart = lines[i].find('(')
            pend = lines[i].find(')')
        if pstart != -1 and pend == -1:
            lines[i] = line.replace(line[pstart:], '')
        elif pstart == -1 and pend != -1:
            lines[i] = line.replace(line[:pend+1], '')     
    return lines


def print_dialogue(dialogue):
    for line in dialogue:
        print(line)


def get_dialogue(lines, characters, dialogue_range):
    dialogue = []
    current_character = None
    for line in lines:
        if not line:
            continue
        if not line.replace('</b>','').strip(' '):
            continue

        if line[0] == '<':
            possible_character = line.replace('<b>','').replace('</b>','').strip(' ')
            if possible_character in characters:
                if current_character != possible_character:
                    current_character = possible_character
                    dialogue.append(current_character)
            else:
                current_character = None
            continue

        if not current_character:
            continue

        blank_length = len(line)-len(line.lstrip(' '))
        if dialogue_range[0] <= blank_length <= dialogue_range[1]:
            dialogue.append(line)
    return dialogue


def split_to_lines(text, test:int=None):
    lines = []
    if test:
        for line in text[:test]:
            lines.extend(str(line).splitlines())
        return lines
    for line in text:
        lines.extend(str(line).splitlines())
    return lines


def get_raw_text(soup):
    return soup.find('pre').contents


def get_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    return soup


if __name__ == '__main__':
    main()