#!/usr/bin/env python
# encoding: utf-8

# http://stackoverflow.com/questions/42558/python-and-the-singleton-pattern

from persister import Persister
from query import Query

class SearchSingleton(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SearchSingleton, cls).__new__(cls, *args, **kwargs)
            cls._instance.index = Persister("/tmp/index").load()
            print "Index length", len(cls._instance.index)
            #print "Index", cls._instance.index.items()
            #for k, v in cls._instance.index.items():
            #    print " "
            #    print k
            #    print v
        return cls._instance

    def query(self, question):
        return Query(self.index).multi_lookup(question)

