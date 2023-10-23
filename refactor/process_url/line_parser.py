from .text_container import TextContainer

class LineParser(TextContainer):
    def __init__(self, text):
        super().__init__(text)
        self.preprocess_text()

    def preprocess_text(self):
        self.remove_non_dialogue()
        self.remove_start()
        self.remove_repeated_characters()


    def remove_non_dialogue(self):
        dialogue = []
        writing = True
        previous_whitespace = 0
        for line in self.text:
            if self.line_is_bold(line):
                if len(dialogue) != 0 and self.line_is_bold(dialogue[-1]):
                    dialogue.pop()
                dialogue.append(line)
                continue
            current_whitespace = len(line)-len(line.lstrip(' '))
            if current_whitespace > previous_whitespace:
                writing = True
            if current_whitespace < previous_whitespace:
                writing = False
            previous_whitespace = current_whitespace
            if writing:
                dialogue.append(line)
        self.text = dialogue

    def remove_start(self):
        start_end_index = 0
        while self.line_is_bold([self.text[start_end_index]]):
            start_end_index += 1
        self.text = self.text[start_end_index + 1:]


    def remove_repeated_characters(self):
        i = 0
        current_character = None
        while i in range(len(self.text)):
            if self.text[i] == current_character:
                self.text[i] = ""
            if self.line_is_bold(self.text[i]):
                current_character = self.text[i]
            i += 1

        while "" in self.text:
            self.text.remove("")

    def get_prompts_and_responses(self, character):
        i = 0
        for line in self.text:
            i += 1
            if self.line_is_character_line(line, character):
                break
        prompt_start = i
        response_start = i + 1
        pairs = []
        while i in range(len(self.text)):
            if self.line_is_character_line(self.text[i], character):
                prompt = (" ".join(map(lambda line: line.strip(), self.text[prompt_start+1:i])))
                response_start = i
                i += 1
                while not self.line_is_bold(self.text[i]):
                    i += 1
                response = (" ".join(map(lambda line: line.strip(),self.text[response_start+1:i])))
                pairs.append({"prompt":prompt,"response":response})
            if self.line_is_bold(self.text[i]):
                prompt_start = i
            i += 1
        return pairs





            
