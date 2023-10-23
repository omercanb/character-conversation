class TextContainer:
    def __init__(self, text):
        self.text = text
    
    def get_bold_lines(self):
        return map(self.strip_bold_line, filter(self.line_is_bold, self.text))

    def line_is_bold(self, line):
        return ('<b>' in line or '</b>' in line) and len(self.strip_bold_line(line)) != 0
    
    def strip_bold_line(self, bold_line):
        return bold_line.replace('<b>','').replace('</b>','').strip()
    
    def line_is_character_line(self, line, character):
        return self.line_is_bold(line) and self.strip_bold_line(line).replace(character, "") == ""