from ketchlip.query import Query

__author__ = 'magnus'

import unittest

class QueryTest(unittest.TestCase):
    def setUp(self):
        self.index = {"become": [[10, 'http://a.com'], [100, 'http://a.com'], [20, 'http://b.com'], [10, 'http://c.com'], [10, 'http://d.com']],
        "june":[[19, 'http://b.com'],  [21, 'http://b.com'], [10, 'http://c.com']],
        "variation": [[11, 'http://b.com'], [22, 'http://b.com'], [42, 'http://b.com'], [10, 'http://c.com'], [10, 'http://d.com']],
        "aweful": [[23, 'http://b.com']]}
        self.query = Query(self.index)

    def test_empty(self):
        self.assertEqual([], self.query.multi_lookup([]))

    def test_empty_string(self):
        self.assertEqual([], self.query.multi_lookup([""]))
        self.assertEqual([], self.query.multi_lookup(['']))

    def test_single_word(self):
        q = ["become"]
        self.assertEqual(['http://a.com', 'http://c.com', 'http://d.com', 'http://b.com'], self.query.multi_lookup(q))

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
