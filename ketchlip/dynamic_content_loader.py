#!/usr/bin/env python
# encoding: utf-8

class DynamicContentLoader:

    def load(self, page):
        f = open("./www/" + page, "r")
        text = f.read()
        f.close()
        return text

