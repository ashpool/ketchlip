#-*- coding: utf-8 -*-

from ketchlip.word import Word

class Sentence:

    def __init__(self, sentence):
        self.sentence = sentence

    def sanitize(self):
        ret = []
        s = str(self.sentence)
        for word in s.split():
            ret += Word(word).slugify(lower=False)
        return " ".join(ret).strip()