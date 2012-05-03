import tweepy
from ketchlip.helpers.config import Config
from ketchlip.tweet_scanner import TweetScanner
from ketchlip.helpers import klogger, config

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

        klogger.info("Scanning " + api.me().name + " friends timeline")

        TweetScanner(conf).run_scan(api)

    except KeyboardInterrupt:
        klogger.info('^C received, shutting down tweet scanner')


if __name__ == "__main__":
    main()