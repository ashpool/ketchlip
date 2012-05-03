import unittest
from ketchlip.helpers import config

class ConfigTest(unittest.TestCase):

    def test_read_from_config_file(self):
        self.assertEqual("ignore_this", config.config.test_property)

if __name__ == '__main__':
    unittest.main()
