#-*- coding: utf-8 -*-

import unittest
import urllib2
from mock import Mock
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
        content = "<html><body>a brown fox</body></html>"
        indexer.add_page_to_index(index, url, content)
        self.assertEqual({u'a': [[0, 'http://dn.se']], u'brown': [[1, 'http://dn.se']], u'fox': [[2, 'http://dn.se']]}, index)

    def test_add_page_to_index_with_too_long_word(self):
        indexer = Indexer()
        index = {}
        url = "http://dn.se"
        content = "<html><body>a brown porcupinesporcupinesporcupinesporcupinesporcupinesporcupines</body></html>"
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

    def test_crawl(self):

        html = """
        <html>
            <head>
                <title>Python is fun!</title>
            </head>
            <body>
                <div>Python is similar to Ruby, but different.</div>
            </body>
        </html>
        """

        response_mock = Mock(url="http://expanded_url.com")
        response_mock.read = Mock(return_value=html)
        urllib2.urlopen = Mock(return_value=response_mock)
        url_list = ["http://a.com", "http://b.com", "http://c.com"]

        indexer = Indexer()

        index, graph, url_lookup = indexer.crawl(url_list)

        expected_index = {u'but': [[5, 0], [5, 1], [5, 2]],
            u'different': [[6, 0], [6, 1], [6, 2]],
            u'is': [[1, 0], [1, 1], [1, 2]],
            u'python': [[0, 0], [0, 1], [0, 2]],
            u'ruby': [[4, 0], [4, 1], [4, 2]],
            u'similar': [[2, 0], [2, 1], [2, 2]],
            u'to': [[3, 0], [3, 1], [3, 2]]}

        self.assertEqual(expected_index, index)
        self.assertEqual({}, graph)
        self.assertEqual( ['http://a.com', 'http://expanded_url.com', u'Python is fun', u'\nPython is similar to Ruby, but different.\n'], url_lookup[0])
