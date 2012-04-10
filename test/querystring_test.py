#-*- coding: utf-8 -*-

from ketchlip.querystring import Querystring

import unittest

class QuerystringTest(unittest.TestCase):

    def test_parse_url_with_no_querystring(self):
        page = Querystring("http://localhost:80/hello_world.twp").page()
        self.assertEqual("hello_world.twp", page)

    def test_parse_short_url_with_no_querystring(self):
        page = Querystring("/hello_world.twp").page()
        self.assertEqual("hello_world.twp", page)

    def test_parse_querystring(self):
        page = Querystring("http://localhost:80/hello_world.twp?say=hello").page()
        self.assertEqual("hello_world.twp", page)

    def test_parse_short_querystring(self):
        page = Querystring("/hello_world.twp?say=hello").page()
        self.assertEqual("hello_world.twp", page)

    def test_parse_short_querystring(self):
        page = Querystring("http://localhost/search.twp?search=").page()
        self.assertEqual("search.twp", page)

    def test_parse_incorrect_query_string(self):
        page = Querystring("http://localhost:80/hello_world.asp").page()
        self.assertIsNone(page)

    def test_parse_empty_query_string(self):
        page = Querystring("").page()
        self.assertIsNone(page)

    def test_get_values(self):
        values = Querystring("http://localhost:80/seach.asp?search=hello+world").get_values("search")
        self.assertEqual(["hello", "world"], values)

    def test_get_values_with_not_querystring(self):
        values = Querystring("http://localhost:80/seach.asp").get_values("search")
        self.assertEqual([], values)


if __name__ == '__main__':
    unittest.main()
