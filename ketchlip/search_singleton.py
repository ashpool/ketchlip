#-*- coding: utf-8 -*-

# http://stackoverflow.com/questions/42558/python-and-the-singleton-pattern
from utils import klogger
from utils.persister import Persister
from query import Query

class SearchSingleton(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SearchSingleton, cls).__new__(cls, *args, **kwargs)
            cls._instance.index = {}
        return cls._instance

    # todo remove default values?
    def load(self, index_file = "/tmp/index", url_lookup_file = "/tmp/url_lookup"):
        self.index = Persister(index_file).load()
        self.url_lookup = Persister(url_lookup_file).load()
        klogger.info("Index length " + str(len(self.index)))
        klogger.info("URL lookup length " + str(len(self.url_lookup)))

    def query(self, question):
        return Query(self.index, self.url_lookup).multi_lookup(question)

