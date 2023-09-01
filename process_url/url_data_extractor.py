import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import random

from process_url.character_extractor import get_characters
import process_url.bold_utils as bold_utils
import process_url.line_utils as line_utils

bold_tag = "<bold>"

def get_url_dialogue(url):
    text = get_raw_text(get_soup(url))
    lines = line_utils.prepeare_lines(text)
    characters = get_characters(bold_utils.get_bold_lines(lines), mention_number = 10)
    dialogue = get_dialogue(lines, characters)
    dialogue_dict = get_dialoague_dict(dialogue, characters)
    return dialogue_dict

def testing(url):
    text = get_raw_text(get_soup(url))
    lines = remove_bolds_not_followed_by_dialogue(remove_non_dialogue(line_utils.prepeare_lines(text)))
    character = "JOKER"
    lines = remove_repeated_characters(remove_start(lines, character))
    pairs = get_character_prompts_and_responses(lines, character)
    
    for line in lines:
        print(line)
    print_pairs(pairs)

def bolded(word):
    return f"{bold_tag} {word}"

def remove_start(lines, character):
    after_title = 0
    while bold_tag in lines[after_title]:
        after_title += 1
    return lines[lines[after_title:].index(bolded(character))+after_title:]

def print_pairs(pairs):
    for pair in pairs:
        print(f"Prompt: {pair['prompt']}")
        print(f"Response: {pair['response']}")
        print()

    


def get_character_prompts_and_responses(lines, character):
    #Track where a bold line starts
    #If a bold line is joker add the space from the start to joker as prompt
    #Continue until a bold line that is not joker followed by a non bold line
    #bold start = 0
    #promt_response_pair = dict()
    #found prompt = False
    #found response = False
    #loop through all lines:
    #   if a line is the character line:
    #       prompt  = bold start (not inclusive) through current index (not inclusive)
    #       character start = index
#           if prompt empty:
    #           continue
    #       search for the end of joker
    #       while this line is not bold and the previous line is bold:
    #           increase index
    #       response = character start through index
    #       
    #   else if a line is bold:
    #        bold start = current line index
    i = 0
    bold_start = 0
    character_start = 1
    prompt = ""
    response = ""
    pairs = []
    while i in range(len(lines[1:])):
        if lines[i] == bolded(character):
            prompt = (" ".join(lines[bold_start+1:i]))
            character_start = i
            while not is_bold(lines[i]) or lines[i] == bolded(character):
                i += 1
            response = (" ".join(lines[character_start+1:i]))
            pairs.append({"prompt":prompt,"response":response})
        if is_bold(lines[i]):
            bold_start = i
        i += 1
    return pairs


def remove_repeated_characters(lines):
    i = 0
    current_character = None
    while i in range(len(lines)):
        if lines[i] == current_character:
            lines[i] = ""
        if is_bold(lines[i]):
            current_character = lines[i]
        i += 1
    return remove_empty_lines(lines)


def remove_bolds_not_followed_by_dialogue(lines):
    i = 0

    for i in range(len(lines)):
        if i == len(lines)-1:
            continue
        if is_bold(lines[i]) and is_bold(lines[i+1]):
            lines[i] = ""
    return remove_empty_lines(lines)


def remove_empty_lines(lines):
    return list(filter(lambda x: x != "",lines))


def is_bold(line):
    return bold_tag in line

def remove_lines_with_bold_tags(lines):
    return list(filter(lambda x: bold_tag not in x, lines))

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


def test_get_dialogue_and_characters(lines):
    dialogue = []
    current_character = None
    writing = True
    previous_whitespace = 0
    characters = []

    for line in lines:

        if bold_utils.line_is_bold(line):
            possible_character = bold_utils.remove_bold_tags(line).strip()
            if possible_character == '': 
                continue
            # if possible_character not in characters: 
            #     current_character = None
            #     continue
            # if current_character != possible_character:
            #     current_character = possible_character
            #     dialogue.append(current_character)
            current_character = possible_character
            print(bold_utils.remove_bold_tags(line).strip())
            continue


        if not current_character:
            continue
        
        preceding_whitespace_length = line_utils.get_preceding_whitespace_length(line)
        if preceding_whitespace_length > previous_whitespace:
            writing = True
        if preceding_whitespace_length < previous_whitespace:
            writing = False
        previous_whitespace = preceding_whitespace_length
        if writing:
            dialogue.append(line)
            if current_character not in characters:
                characters.append(current_character)
        print(f'{writing}',line)
    return dialogue, characters


def remove_non_dialogue(lines):
    dialogue = []
    writing = True
    previous_whitespace = 0
    for line in lines:
        if bold_utils.line_is_bold(line):
            bold_line = bold_utils.remove_bold_tags(line).strip()
            if bold_line != "":
                dialogue.append(f"{bold_tag} {bold_line}")
            continue
        preceding_whitespace_length = line_utils.get_preceding_whitespace_length(line)
        if preceding_whitespace_length > previous_whitespace:
            writing = True
        if preceding_whitespace_length < previous_whitespace:
            writing = False
        previous_whitespace = preceding_whitespace_length
        if writing:
            dialogue.append(line.strip())
    return dialogue


def get_dialogue(lines, characters):
    dialogue = []
    current_character = None
    writing = True
    previous_whitespace = 0
    for line in lines:

        if bold_utils.line_is_bold(line):
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