import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import random

from process_url.character_extractor import get_characters
from process_url.bold_utils import get_bold_lines, remove_bold_tags, line_is_bold
from process_url.line_utils import prepeare_lines, get_preceding_whitespace_length

def get_url_dialogue(url):
    text = get_raw_text(get_soup(url))
    lines = prepeare_lines(text)
    characters = get_characters(get_bold_lines(lines), mention_number = 10)
    dialogue = get_dialogue(lines, characters)
    dialogue_dict = get_dialoague_dict(dialogue, characters)
    return dialogue_dict


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


def get_dialogue(lines, characters):
    dialogue = []
    current_character = None
    writing = True
    previous_whitespace = 0
    for line in lines:

        if line_is_bold(line):
            possible_character = remove_bold_tags(line).strip()
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
        
        preceding_whitespace_length = get_preceding_whitespace_length(line)
        if preceding_whitespace_length > previous_whitespace:
            writing = True
        if preceding_whitespace_length < previous_whitespace:
            writing = False
        previous_whitespace = preceding_whitespace_length
        if writing:
            dialogue.append(line)
    return dialogue


def get_raw_text(soup, test = False):
    if not test:
        return max(soup.find_all('pre'),key=lambda x: len(x))
    if test:
        max(soup.find_all('pre'),key=lambda x: len(x))

def get_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    return soup


if __name__ == '__main__':
    url = input()
    url = 'https://imsdb.com/scripts/Joker.html'
    d = get_url_dialogue(url)
    print(d)