import re

class HtmlCleaner:
    def __init__(self, html):
        self.html = html

    def clean_html(self):
        self.html = [str(line) for line in self.html]
        self.remove_parantheses()
        self.split_to_lines()
        self.remove_empty_lines()
        self.remove_revisions()
        


    def remove_parantheses(self):
        for i,line in enumerate(self.html):
            while self.open_close_parantheses_exists(self.html[i]):
                pstart,pend = self.find_parantheses_index(self.html[i])
                self.html[i] = self.html[i].replace(self.html[i][pstart:pend+1], '')
    

    def find_parantheses_index(self, line: str):
        return line.find('('),line.find(')')
    

    def open_close_parantheses_exists(self, line: str):
        pstart,pend = self.find_parantheses_index(line)
        return pstart != -1 and pend != -1
    
    def split_to_lines(self):
        lines = []
        for line in self.html:
            lines.extend(line.splitlines())
        self.html = lines

    def remove_empty_lines(self):
        self.html = list(filter(lambda line: line.strip() != '' and len(line) != 0, self.html))
        self.html = list(filter(lambda line: len(line.replace('<b>','').replace('</b>','').strip()) != 0, self.html))

    def remove_revisions(self):
        #For example: https://imsdb.com/scripts/La-La-Land.html
        exp = "\s*Revision\s*[0-9][0-9]*\."
        self.html = list(filter(lambda line: re.match(exp, line.strip()) == None, self.html))
    
        

        