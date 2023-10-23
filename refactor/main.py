from process_url.html_extractor import HtmlExtractor
from process_url.html_cleaner import HtmlCleaner
from process_url.character_selector import CharacterSelector
from process_url.line_parser import LineParser
from save_csv import save_csv, get_path
from train import MovieDialogueTrainer
from conversation import UserConversation

import transformers
transformers.logging.set_verbosity_warning()


import csv
import os
import sys
from string import capwords
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import prompt

url = "https://imsdb.com/scripts/Joker.html"
movie = "Joker"

def main():
    if movie_models_exist(movie):
        character = choose_existing_character(movie)
        if character != "Other":
            model_path = os.path.join(get_save_directory(movie), character)
            converse(model_path, character)
            return

    text = get_clean_html(url)
    character = choose_new_character(text)
    parser = LineParser(text)

    prompts_and_responses = parser.get_prompts_and_responses(character)
    csv_path = get_path(character, movie)
    save_csv(prompts_and_responses, character, movie)

    character = capwords(character)
    trainer = MovieDialogueTrainer(csv_path, character, movie)
    trainer.train_save_model()

    model_path = trainer.get_save_path()
    converse(model_path, character)


def converse(model_path, character):
    conversation = UserConversation(model_path, character)

    while True:
        user_line = input("You: ")
        response = conversation.speak(user_line)
        print(f"{character}: ", end="")
        print(response)


def movie_models_exist(movie):
    path = get_save_directory(movie)
    models = os.listdir(path)
    return len(models) > 0


def get_save_directory(movie):
    return os.path.join("models", "finetuned", "movies", movie)


def choose_existing_character(movie):
    path = get_save_directory(movie)
    characters = os.listdir(path)
    print("Choose one of the following characters or type other to load other movie characters: ")
    characters.append("Other")
    choices = characters
    print(", ".join(choices))
    completer = WordCompleter(choices, ignore_case=True)
    character = prompt("Character: ", completer=completer)
    return character


def choose_new_character(text):
    selector = CharacterSelector(text)
    print("Choose one of the following characters.")
    possible_characters = selector.get_characters(mention_number = 20)
    possible_characters = list(map(capwords, possible_characters))
    print(", ".join(possible_characters))
    completer = WordCompleter(possible_characters, ignore_case=True)
    character = prompt("Character: ", completer=completer)
    character = character.upper()
    return character

def get_clean_html(url):
    jokerHtmlExtractor = HtmlExtractor(url)
    cleaner = HtmlCleaner(jokerHtmlExtractor.html)
    cleaner.clean_html()
    return cleaner.html



if __name__ == "__main__":
    main()