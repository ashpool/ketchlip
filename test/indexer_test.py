#!/usr/bin/env python
# encoding: utf-8

import unittest
from ketchlip.indexer import Indexer


class IndexerTest(unittest.TestCase):

    def test_add_to_index(self):
        indexer = Indexer()
        index = {}
        keyword = "keyword"
        url = "http://dn.se"

        indexer.add_to_index(index, keyword, 42, url)
        self.assertEqual({'keyword': [[42, 'http://dn.se']]}, index)

        indexer.add_to_index(index, keyword, 43, url)
        self.assertEqual({'keyword': [[42, 'http://dn.se'], [43, 'http://dn.se']]}, index)

    def test_add_page_to_index(self):
        indexer = Indexer()
        index = {}
        url = "http://dn.se"
        content = "a brown fox"
        indexer.add_page_to_index(index, url, content)
        self.assertEqual({u'a': [[0, 'http://dn.se']], u'brown': [[1, 'http://dn.se']], u'fox': [[2, 'http://dn.se']]}, index)

    def test_add_page_to_index_with_too_long_word(self):
        indexer = Indexer()
        index = {}
        url = "http://dn.se"
        content = "a brown porcupinesporcupinesporcupinesporcupinesporcupinesporcupines"
        indexer.add_page_to_index(index, url, content)
        self.assertEqual({u'a': [[0, 'http://dn.se']], u'brown': [[1, 'http://dn.se']]}, index)