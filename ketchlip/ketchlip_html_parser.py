#-*- coding: utf-8 -*-

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

    def description(self, max_length = None):
        soup = self.soup_factory(self.content)
        meta_descriptions = soup.findAll('meta', {'name':'description'})
        description = ''
        for tag in meta_descriptions:
            if tag.has_key('content'):
                description += tag['content']
        if max_length and len(description) > max_length:
            description = description[:max_length].strip() + " ..."
        return description

    def text(self):
        soup = self.soup_factory(self.content)
        if not soup.html or not soup.html.body:
            return ""
        body_text = soup.html.body.get_text(separator=" ", strip=True).strip()
        pat = re.compile(r'\s+')
        return pat.sub(' ', body_text)
