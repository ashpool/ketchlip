import ConfigParser
import tweepy
from ketchlip.tweet_scanner import TweetScanner
from ketchlip.helpers import klogger
from ketchlip.helpers.persister import Persister

def main():
    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read("./ketchlip.cfg")

        CONSUMER_KEY = cfg.get("Twitter", "CONSUMER_KEY")
        CONSUMER_SECRET = cfg.get("Twitter", "CONSUMER_SECRET")
        ACCESS_TOKEN = cfg.get("Twitter", "ACCESS_TOKEN")
        ACCESS_TOKEN_SECRET = cfg.get("Twitter", "ACCESS_TOKEN_SECRET")

        BASE_DIR = cfg.get("Files", "BASE_DIR")

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        api = tweepy.API(auth)

        last_status_processed = Persister(BASE_DIR + "/last_status_processed.txt").load()

        klogger.info("Scanning " + api.me().name + " friends timeline")
        klogger.info("Base directory " + str(BASE_DIR))
        klogger.info("Last status processed " + str(last_status_processed))

        TweetScanner().run_scan(api, last_status_processed = last_status_processed, base_dir = BASE_DIR)

    except KeyboardInterrupt:
        klogger.info('^C received, shutting down tweet scanner')


if __name__ == "__main__":
    main()