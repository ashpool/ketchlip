import unittest
from ketchlip.helpers.config import Config
from ketchlip.tweet_scanner import TweetScanner


class TweetScannerTest(unittest.TestCase):

    def setUp(self):
        params ={ "base_dir": "/tmp/",
        "tweet_file": "tweet_file",
        "last_status_processed_file": "last_status_processed"}
        self.config = Config(params)

    def test_get_all_links(self):
        text = "New copyright law #LeyLleras2 in Colombia seriously threatens #netfreedom - http://t.co/TDy99tuL"
        self.assertEqual(["http://t.co/TDy99tuL"], TweetScanner(self.config).get_all_links(text))

        text = "Not sure whether to laugh or cry: http://t.co/NgloHWqe The Rejection Generator helps writers http://t.co/qUuAjem5"
        self.assertEqual(["http://t.co/NgloHWqe", "http://t.co/qUuAjem5"], TweetScanner(self.config).get_all_links(text))

    def test_configuration(self):
        ts = TweetScanner(self.config)
        self.assertEqual(self.config.tweet_file, ts.tweet_file)

    def test_persist(self):
        tweets = ["http://t.co/gfe0Y0li", "http://t.co/ckR0lSQi", "http://t.co/lIc8wM0m"]
        last_status_processed = 1335935402.56

        ts = TweetScanner(self.config)
        ts.persist(tweets, last_status_processed)


if __name__ == '__main__':
    unittest.main()
