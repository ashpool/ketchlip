#-*- coding: utf-8 -*-

import re
from unicodedata import normalize

def remove_html_tags(word):
    pattern = re.compile(r'</?\w.*>')
    return re.sub(pattern, "", word)

class Word:

    def __init__(self, word):
        self.word = word

    def slugify(self, delim=u' ', lower=True):
        _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.:]+')

        text = str(self.word).decode('utf-8')

        text = remove_html_tags(text)

        result = []
        if lower:
            text = text.lower()

        for word in _punct_re.split(text):
            word = normalize('NFKD', word).encode('ascii', 'ignore')
            if word:
                result.append(word)
        return unicode(delim.join(result)).split()
