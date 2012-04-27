#-*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
import cgi

class KetchlipHTMLParser:

    def __init__(self, content = ""):
        self.content = content
        self.soup = None

    def get_soup(self):
        if not self.soup:
            self.soup = self.soup_factory(self.content)
        return self.soup

    def soup_factory(self, content):
        content = self.prettify(content)
        soup = BeautifulSoup(content)
        soup.prettify()
        return BeautifulSoup(soup.prettify())

    def title(self):
        soup = self.get_soup()
        if not soup.html or not soup.html.head or not soup.html.head.title:
            return ""
        #return self.html_encode(soup.html.head.title.get_text().strip())
        return soup.html.head.title.get_text().strip()

    def description(self, max_length = None):
        soup = self.get_soup()
        meta_descriptions = soup.findAll('meta', {'name':'description'})
        description = ''
        for tag in meta_descriptions:
            if tag.has_key('content'):
                description += tag['content']
        if max_length and len(description) > max_length:
            description = description[:max_length].strip() + " ..."
        #return self.html_encode(description)
        return description

    def text(self):
        soup = self.get_soup()
        if not soup.html or not soup.html.body:
            return ""
        body_text = soup.html.body.get_text(separator=" ", strip=True).strip()
        pat = re.compile(r'\s+')
        return pat.sub(' ', body_text)

    def prettify(self, html):
        """
        BeautifulSoup doesn't like malformatted tags like <scr + ipt>
        """
        return re.subn(r'<((sc.*?pt)).*?</\1>(?s)', '', html)[0]

    def html_encode(self, text):
        return cgi.escape(text.decode('utf-8')).encode('ascii', 'xmlcharrefreplace')