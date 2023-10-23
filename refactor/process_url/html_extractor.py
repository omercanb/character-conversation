from bs4 import BeautifulSoup
import requests

class HtmlExtractor:
    def __init__(self, url):
        self.url = url
        self.html = self.get_html()

    def get_html(self):
        response = requests.get(self.url)
        #check response
        html = BeautifulSoup(response.content,'html.parser')
        html = max(html.find_all('pre'),key=lambda x: len(x))
        return html
    
    def __str__(self):
        return self.html.prettify()
    