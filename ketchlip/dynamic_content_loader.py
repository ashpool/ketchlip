#!/usr/bin/env python
# encoding: utf-8

class DynamicContentLoader:

    def load(self, page, base_dir = "./www/"):
        f = open(base_dir + page, "r")
        text = f.read()
        f.close()
        return text

