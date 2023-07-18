"""
All processes involving extracting the characters given the bold lines of a script
"""
from collections import defaultdict

from consts import movie_transitions


def get_characters(bold_lines,mention_number):
    mentions = clean_mentions(count_mentions(bold_lines))
    characters = filter_mentions(mentions,mention_number)
    return characters


def clean_mentions(mentions):
    return remove_transition_mentions(remove_empty_mentions(mentions))


def count_mentions(bold_lines):
    mentions = defaultdict(lambda:0)
    for line in bold_lines:
        mentions[line] += 1
    return mentions


def filter_mentions(mentions,mention_number):
    return [character for character,mention in mentions.items() if mention >= mention_number]


def remove_empty_mentions(mentions):
    if '' in mentions:
        del mentions['']
    return mentions


def remove_transition_mentions(mentions):
    for transition in movie_transitions:
        if transition in mentions:
            del mentions[transition]
    return mentions
