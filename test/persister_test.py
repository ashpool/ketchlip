#-*- coding: utf-8 -*-

import unittest
from ketchlip.persister import Persister


class PersisterTest(unittest.TestCase):
    def setUp(self):
        self.persister = Persister("/tmp/persister_test")

    def save_load(self, message):
        self.persister.save(message)
        return self.persister.load()

    def test_save_load(self):
        message = "Hello World!"
        self.assertEqual(message, self.save_load(message))

    def test_unicode(self):
        message = "ÖkuarneåÅäÄöÖ"
        self.assertEqual(message, self.save_load(message))

    def test_dictionary(self):
        d = {'key': "value"}
        self.assertEqual(d, self.save_load(d))


if __name__ == '__main__':
    unittest.main()