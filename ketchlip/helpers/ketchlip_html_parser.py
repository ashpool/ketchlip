#-*- coding: utf-8 -*-

import re
import HTMLParser
from bs4 import BeautifulSoup


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

    def content_tag(self):
        soup = self.get_soup()
        meta_descriptions = soup.findAll('meta', {'name':'description'})
        for tag in meta_descriptions:
            if tag.has_key('content'):
                return tag

    def charset(self):
        """
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        """
        soup = self.get_soup()
        meta_descriptions = soup.findAll('meta', {'content':'text/html'})
        for tag in meta_descriptions:
            if tag.has_key('charset'):
                print 'tag["charset"]', tag["charset"]
                return tag["charset"].lower()
        print 'DEFAULT', 'utf-8'
        return 'utf-8'

    def title(self):
        soup = self.get_soup()
        if not soup.html or not soup.html.head or not soup.html.head.title:
            return ""
        return soup.html.head.title.get_text().strip()

    def description(self, max_length = None):
        description = ''
        tag = self.content_tag()
        if tag and tag.has_key('content'):
            description += tag['content']
        if max_length and len(description) > max_length:
            description = description[:max_length].strip() + " ..."
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
