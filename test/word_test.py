#!/usr/bin/env python
# encoding: utf-8
from ketchlip import word

from ketchlip.word import Word

__author__ = 'magnus'

import unittest

class WordTest(unittest.TestCase):
    def test_slugify(self):
        word = Word(".Unclean:")
        self.assertEqual(["unclean"], word.slugify())

    def test_slugify_with_non_ascii_chars(self):
        word = Word(".UncleanÅÄÖ:")
        self.assertEqual(["uncleanaao"], word.slugify())

    def test_slugify_with_dirty_middle(self):
        word = Word('Reality">Mitt')
        self.assertEqual(['reality', 'mitt'], word.slugify())

    def test_remove_left_html_paragraph(self):
        self.assertEqual('Mitt', word.remove_html_tags('<p>Mitt'))

    def test_remove_right_unescaped_html_paragraph(self):
        self.assertEqual('Mitt', word.remove_html_tags('Mitt<p>'))

    def test_remove_right_escaped_html_paragraph(self):
        self.assertEqual('Mitt', word.remove_html_tags('Mitt</p>'))




