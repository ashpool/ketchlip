#-*- coding: utf-8 -*-

from word import Word

class Sentence:

    def __init__(self, sentence):
        self.sentence = sentence

    # todo fix this method
    def sanitize(self):
        ret = []
        s = str(self.sentence.encode("utf-8"))
        for word in s.split():
            ret += Word(word).slugify(lower=False)
        return " ".join(ret).strip()