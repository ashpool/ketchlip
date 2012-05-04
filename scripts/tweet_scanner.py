import tweepy
from ketchlip.helpers.config import Config
from ketchlip.tweet_scanner import TweetScanner
from ketchlip.helpers import klogger, config

def main():
    try:
        klogger.logger = klogger.get_logger("ketchlip", "tweet_scanner.log")

        base_dir = config.config.base_dir

        conf = Config()
        conf.base_dir = base_dir
        conf.tweet_file = "tweets.txt"
        conf.last_status_processed_file = "last_status_processed.txt"

        auth = tweepy.OAuthHandler(config.config.consumer_key, config.config.consumer_secret)
        auth.set_access_token(config.config.access_token, config.config.access_token_secret)

        api = tweepy.API(auth)

        klogger.info("Scanning " + api.me().name + " friends timeline")

        TweetScanner(conf).run_scan(api)

    except KeyboardInterrupt:
        klogger.info('^C received, shutting down tweet scanner')


if __name__ == "__main__":
    main()