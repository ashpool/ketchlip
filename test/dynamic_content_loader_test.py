#!/usr/bin/env python
# encoding: utf-8

import unittest
from ketchlip.dynamic_content_loader import DynamicContentLoader


class DynamicContentLoaderTest(unittest.TestCase):
    def setUp(self):
        self.loader = DynamicContentLoader()
        self.hello_world_content = "<p>Hello World!</p>"

    def test_load(self):
        content = self.loader.load("hello_world.twp", "./www/")
        self.assertEqual(self.hello_world_content, content)

if __name__ == '__main__':
    unittest.main()