import re
from bs4 import BeautifulSoup

class KetchlipHTMLParser:

    def __init__(self, content):
        self.content = content

    def soup_factory(self, content):
        soup = BeautifulSoup(content)
        soup.prettify()
        return BeautifulSoup(soup.prettify())

    def title(self):
        soup = self.soup_factory(self.content)
        if not soup.html or not soup.html.head or not soup.html.head.title:
            return ""
        return soup.html.head.title.get_text().strip()

    def text(self):
        soup = self.soup_factory(self.content)
        if not soup.html or not soup.html.body:
            return ""
        body_text = soup.html.body.get_text(separator=" ", strip=True).strip()
        pat = re.compile(r'\s+')
        return pat.sub(' ', body_text)
