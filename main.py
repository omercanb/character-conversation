import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import random

import character_extractor
import bold_utils
import line_lenght_analyzer
import line_utils


def main():
    url = "https://imsdb.com/scripts/Joker.html"
    text = get_raw_text(get_soup(url))
    lines = line_utils.remove_parantheses(line_utils.split_to_lines(text))
    characters = character_extractor.get_characters(bold_utils.get_bold_lines(lines), mention_number = 20)
    dialogue = get_dialogue(lines, characters, dialogue_range = (10,18))
    dialogue_dict = get_dialoague_dict(dialogue, characters)
    print_dialogue(dialogue)


def get_dialoague_dict(dialogue, characters):
    dialogue_dict = defaultdict(lambda:[])
    current_character = dialogue[0]
    for line in dialogue:
        if line in characters:
            current_character = line
            continue
        dialogue_dict[current_character].append(line.strip())
    return dialogue_dict



def print_dialogue(dialogue):
    for line in dialogue:
        print(line)


def get_dialogue(lines, characters, dialogue_range):
    dialogue = []
    current_character = None
    for line in lines:

        if bold_utils.line_bold_open(line):
            possible_character = bold_utils.remove_bold_tags(line).strip()
            if possible_character == '': 
                continue
            if possible_character not in characters: 
                current_character = None
                continue
            if current_character != possible_character:
                current_character = possible_character
                dialogue.append(current_character)
            continue

        if not current_character:
            continue
        
        preceding_whitespace_length = line_utils.get_preceding_whitespace_length(line)
        if dialogue_range[0] <= preceding_whitespace_length <= dialogue_range[1]:
            dialogue.append(line)
    return dialogue



def get_raw_text(soup, test = False):
    if not test:
        return soup.find('pre').contents
    if test:
        soup.find('pre').contents[:test]


def get_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    return soup


if __name__ == '__main__':
    main()