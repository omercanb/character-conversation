from collections import Counter
from .text_container import TextContainer

class CharacterSelector(TextContainer):
    def __init__(self, text):
        super().__init__(text)


    def get_characters(self, mention_number):
        counts = Counter(self.get_bold_lines())
        counts = dict(filter(lambda x: x[0] not in movie_transitions and x[1] >= mention_number, counts.items()))
        characters = counts.keys()
        return characters
    

movie_transitions = {
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
    "CONTINUED:"
}