import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import random


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
    text = get_script(soup)
    lines = get_lines(text, test=1000)
    lines = remove_parantheses(lines)
    characters = get_characters(lines, mention_number = 20)
    dialogue = get_dialogue(lines, characters)
    dialogue_dict = get_dialoague_dict(dialogue, characters)
    while True:
        print(characters)
        char = input("Choose character: ")
        print(random.choice(dialogue_dict[char.upper()]))


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
        if '(' in line:
            if ')' in line:
                lines[i] = line.replace(line[line.find('('):line.find(')')+1], '')
    return lines


def get_characters(lines,mention_number):
    lengths = get_bold_lengths(lines)
    mentions = defaultdict(lambda:0)
    for length in lengths:
        for line in lengths[length]:
            mentions[line.strip()] += 1
    if '' in mentions:
        del mentions['']
    for transition in transitions:
        if transition in mentions:
            del mentions[transition]
    mentions = {character:mention for character,mention in mentions.items() if mention >= mention_number}
    return list(mentions.keys())

def print_dialogue(dialogue):
    for line in dialogue:
        print(line)

def get_dialogue(lines, characters):
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
        if 10 <= blank_length <= 18:
            dialogue.append(line)
    return dialogue


def get_lines(text, test:int=None):
    lines = []
    if test:
        for line in text[:test]:
            lines.extend(str(line).splitlines())
        return lines
    for line in text:
        lines.extend(str(line).splitlines())
    return lines


def get_script(soup):
    return soup.find('pre').contents


def get_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    return soup


def get_blankspace_lengths(lines, print_values=False):  
    blank_lengths = defaultdict(lambda:[])
    for line in lines:
        blank_length = len(line)-len(line.lstrip(' '))
        blank_lengths[blank_length].append(line)
    if print_values:
        for key in blank_lengths:
            for ex in blank_lengths[key][:2]:
                print(key,end=':  ')
                print(ex)


def get_bold_lengths(lines, print_values=False):
    blank_lengths = defaultdict(lambda:[])
    for line in lines:
        if not line:
            continue
        if line[0] != '<':
            continue
        line = line.replace('<b>','').replace('</b>','')
        blank_length = len(line)-len(line.lstrip(' '))
        blank_lengths[blank_length].append(line)
    if print_values:   
        for key in blank_lengths:
            for ex in blank_lengths[key][:2]:
                print(key,end=':  ')
                print(ex)
    return blank_lengths


if __name__ == '__main__':
    main()