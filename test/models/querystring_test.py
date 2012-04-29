#-*- coding: utf-8 -*-

from ketchlip.models.querystring import Querystring

import unittest

class QuerystringTest(unittest.TestCase):

    def test_parse_url_with_no_querystring(self):
        page = Querystring("http://localhost:80/hello_world").page()
        self.assertEqual("hello_world", page)

    def test_parse_short_url_with_no_querystring(self):
        page = Querystring("/hello_world").page()
        self.assertEqual("hello_world", page)

    def test_parse_querystring(self):
        page = Querystring("http://localhost:80/hello_world?say=hello").page()
        self.assertEqual("hello_world", page)

    def test_parse_short_querystring(self):
        page = Querystring("/hello_world?say=hello").page()
        self.assertEqual("hello_world", page)

    def test_parse_short_querystring(self):
        page = Querystring("http://localhost/search?search=").page()
        self.assertEqual("search", page)

    def test_parse_empty_query_string(self):
        page = Querystring("").page()
        self.assertEqual("", page)

    def test_get_values(self):
        values = Querystring("http://localhost:80/search?search=hello+world").get_values("search")
        self.assertEqual(["hello", "world"], values)

    def test_get_values_with_not_querystring(self):
        values = Querystring("http://localhost:80/search").get_values("search")
        self.assertEqual([], values)


if __name__ == '__main__':
    unittest.main()
