#-*- coding: utf-8 -*-

import unittest
from nose.tools import raises
from ketchlip.helpers.persister import Persister


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

    def test_attempt_to_load_nonexisting_file_should_return_none(self):
        persister = Persister("/tmp/this_file_does_not_exist")
        self.assertIsNone(persister.load())

    def test_default_return(self):
        default_return = {}
        persister = Persister("/tmp/this_file_does_not_exist")
        self.assertEqual(default_return, persister.load(default_return))



if __name__ == '__main__':
    unittest.main()