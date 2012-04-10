#-*- coding: utf-8 -*-

from ketchlip.search_singleton import SearchSingleton

import unittest

class SearchSingletonTest(unittest.TestCase):

    def test_singletonitis(self):
        singleton_a = SearchSingleton()
        singleton_b = SearchSingleton()

        self.assertTrue(singleton_a == singleton_b)


if __name__ == '__main__':
    unittest.main()
