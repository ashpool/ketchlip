#-*- coding: utf-8 -*-

# http://stackoverflow.com/questions/42558/python-and-the-singleton-pattern
import time
from ketchlip.helpers import klogger
from ketchlip.helpers.persister import Persister
from ketchlip.models.query import Query
from time import localtime, strftime

logger = klogger.get_module_logger(__name__)

class SearchSingleton(object):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SearchSingleton, cls).__new__(cls, *args, **kwargs)
            cls._instance.index = {}
        return cls._instance

    def load(self, index_file, url_lookup_file):
        self.load_time = strftime("%Y-%m-%d %H:%M:%S", localtime())
        self.index_file, self.url_lookup_file = index_file, url_lookup_file
        self.index = Persister(self.index_file).load()
        self.url_lookup = Persister(self.url_lookup_file).load()
        logger.info("Index length " + str(len(self.index)))
        logger.info("URL lookup length " + str(len(self.url_lookup)))

    def query(self, question):
        return Query(self.index, self.url_lookup).multi_lookup(question)

    def notify(self, message):
        logger.info(message)
        self.load(self.index_file, self.url_lookup_file)


