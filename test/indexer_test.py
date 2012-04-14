#-*- coding: utf-8 -*-

import unittest
import urllib2
from mock import Mock
from ketchlip.indexer import Indexer, Crawler


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

        html = \
        """<html>
            <head>
                <title>Python is fun!</title>
            </head>
            <body>
                <div>Python is similar to Ruby, but different.</div>
            </body>
        </html>"""

        response_mock = Mock(url="http://expanded_url.com")
        response_mock.read = Mock(return_value=html)
        urllib2.urlopen = Mock(return_value=response_mock)
        url = "http://a.com"

        crawler = Crawler()

        result = crawler.crawl(url)

        expected_result = {'CONTENT': html,
                           'EXPANDED_URL': 'http://expanded_url.com',
                           'TEXT': u'Python is similar to Ruby, but different.',
                           'TITLE': u'Python is fun',
                           'URL': 'http://a.com'}

        self.assertEqual(expected_result, result)
