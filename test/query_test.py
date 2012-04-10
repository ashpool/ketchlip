#-*- coding: utf-8 -*-

from ketchlip.query import Query

import unittest

class QueryTest(unittest.TestCase):
    def setUp(self):
        self.index = {"become": [[10, 0], [100, 0], [20, 1], [10, 2], [10, 3]],
        "june":[[19, 1],  [21, 1], [10, 2]],
        "variation": [[11, 1], [22, 1], [42, 1], [10, 2], [10, 3]],
        "aweful": [[23, 1]]}

        self.url_lookup = {0: 'http://a.com', 1: 'http://b.com', 2: 'http://c.com', 3: 'http://d.com'}
        self.query = Query(self.index, self.url_lookup)

    def test_empty(self):
        self.assertEqual([], self.query.multi_lookup([]))

    def test_empty_string(self):
        self.assertEqual([], self.query.multi_lookup([""]))
        self.assertEqual([], self.query.multi_lookup(['']))

    def test_single_word(self):
        q = ["become"]
        self.assertEqual(['http://a.com', 'http://b.com', 'http://c.com', 'http://d.com'], self.query.multi_lookup(q))

    def test_two_words(self):
        q = ["become", "june"]
        self.assertEqual(['http://b.com', 'http://c.com'], self.query.multi_lookup(q))

    def test_three_words(self):
        q = ["become", "june", "variation"]
        self.assertEqual(['http://b.com', 'http://c.com'], self.query.multi_lookup(q))

    def test_four_words(self):
        q = ["become", "june", "variation", "aweful"]
        self.assertEqual(['http://b.com'], self.query.multi_lookup(q))


if __name__ == '__main__':
    unittest.main()
