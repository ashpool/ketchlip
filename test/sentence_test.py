#-*- coding: utf-8 -*-

from ketchlip.sentence import Sentence

import unittest

class SentenceTest(unittest.TestCase):

    def test_sanitize(self):

        unsanitized = "Google Tablet Release Postponed to July   - Social Barrel"
        sanitized = "Google Tablet Release Postponed to July Social Barrel"

        self.assertEqual(sanitized, Sentence(unsanitized).sanitize())

if __name__ == '__main__':
    unittest.main()
