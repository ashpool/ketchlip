import unittest
from ketchlip import tweet_scanner
from ketchlip.tweet_scanner import TweetScanner

class TweetScannerTest(unittest.TestCase):

    def test_get_all_links(self):
        text = "New copyright law #LeyLleras2 in Colombia seriously threatens #netfreedom - http://t.co/TDy99tuL"
        self.assertEqual(["http://t.co/TDy99tuL"], TweetScanner().get_all_links(text))

        text = "Not sure whether to laugh or cry: http://t.co/NgloHWqe The Rejection Generator helps writers http://t.co/qUuAjem5"
        self.assertEqual(["http://t.co/NgloHWqe", "http://t.co/qUuAjem5"], TweetScanner().get_all_links(text))


if __name__ == '__main__':
    unittest.main()
