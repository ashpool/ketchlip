#-*- coding: utf-8 -*-
from Queue import Queue

import unittest
import urllib2
from mock import Mock
from ketchlip.indexer import Indexer, Crawler


class IndexerTest(unittest.TestCase):

    def test_indexing(self):
        # given
        result = {Crawler.CONTENT: '<html><head><title>some title</title><meta name="description" content="some description"/></head><body><p>some text</p></body></html>',
                  Crawler.EXPANDED_URL: "http://expandedurl.com",
                  Crawler.URL: "http://url.com"}

        # when
        indexer = Indexer()
        indexer.indexing(result)

        # then
        expected_index = {u'description': [[3, 0]],
                          u'some': [[0, 0], [2, 0], [4, 0]],
                          u'text': [[5, 0]],
                          u'title': [[1, 0]]}

        self.assertEqual(expected_index, indexer.index)

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

    def test_mock(self):
        html = """
        <html>
            <head>
                <title>Python is fun!</title>
            </head>
            <body>
                <div><Python is similar to Ruby, but different./div>
            </body>
        </html>
        """

        url = "http://a.com"
        response_mock = Mock(url=url)
        response_mock.read = Mock(return_value=html)

        urllib2.urlopen = Mock(return_value=response_mock)

        resp = urllib2.urlopen("http://a.com")

        self.assertEqual(html, resp.read())
        self.assertEqual(url, resp.url)


