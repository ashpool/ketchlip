#!/usr/bin/env python
# encoding: utf-8

# http://stackoverflow.com/questions/42558/python-and-the-singleton-pattern
import klogger
from persister import Persister
from query import Query

class SearchSingleton(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SearchSingleton, cls).__new__(cls, *args, **kwargs)
            cls._instance.index = {}
        return cls._instance

    def load_index(self, index_file = "/tmp/index"):
        self.index = Persister(index_file).load()
        klogger.info("Index length " + str(len(self.index)))

    def query(self, question):
        return Query(self.index).multi_lookup(question)

