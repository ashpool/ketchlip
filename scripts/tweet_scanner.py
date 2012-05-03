import tweepy
from ketchlip.helpers.config import Config
from ketchlip.tweet_scanner import TweetScanner
from ketchlip.helpers import klogger, config
from ketchlip.helpers.persister import Persister

def main():
    try:
        CONSUMER_KEY = config.config.consumer_key
        CONSUMER_SECRET = config.config.consumer_secret
        ACCESS_TOKEN = config.config.access_token
        ACCESS_TOKEN_SECRET = config.config.access_token_secret

        base_dir = config.config.base_dir

        conf = Config()
        conf.base_dir = base_dir
        conf.tweet_file = "tweets.txt"
        conf.last_status_processed_file = "last_status_processed.txt"

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        api = tweepy.API(auth)

        # todo inline into tweet scanner
        last_status_processed = Persister(base_dir + "/last_status_processed.txt").load()

        klogger.info("Scanning " + api.me().name + " friends timeline")
        klogger.info("Base directory " + str(base_dir))
        klogger.info("Last status processed " + str(last_status_processed))

        TweetScanner(conf).run_scan(api, last_status_processed = last_status_processed)

    except KeyboardInterrupt:
        klogger.info('^C received, shutting down tweet scanner')


if __name__ == "__main__":
    main()