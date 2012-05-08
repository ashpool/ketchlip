#-*- coding: utf-8 -*-

import re
import time
import tweepy
import codecs
from tweepy.error import TweepError
from ketchlip.helpers import klogger
from ketchlip.helpers.persister import Persister

logger = klogger.get_module_logger(__name__)

class TweetScanner():

    def __init__(self, config):
        self.base_dir = config.base_dir
        self.tweet_file = config.tweet_file
        self.last_status_processed_file = config.last_status_processed_file

    def get_all_links(self, text):
        links = []
        pattern = r"((https?):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)"
        expression = re.compile(pattern)
        result = expression.findall(text)
        if result:
            for link in result:
                logger.info("FETCH: " + text)
                links.append(link[0])
        return links

    def scan(self, api, last_status_processed = None):
        BATCH_SIZE = 5
        tweets = []

        while True:
            for status in tweepy.Cursor(api.friends_timeline, since_id=last_status_processed).items(20):
                if last_status_processed is None:
                    last_status_processed = status.id
                    break

                if status.id > last_status_processed:
                    last_status_processed = status.id

                links =  self.get_all_links(status.text)

                if len(links) >= 0:
                    for link in links:
                        tweets.append(link)

                        if len(tweets) > BATCH_SIZE:
                            logger.info("Writing tweets to file")
                            tweets = self.persist(tweets, last_status_processed)

            time.sleep(60)

    def persist(self, tweets, last_status_processed):
        self.persist_tweets(tweets)
        self.persist_last_status_processed(last_status_processed)
        return []

    def persist_tweets(self, tweets):
        f = codecs.open(self.base_dir + self.tweet_file, "a", "utf-8")
        for tweet in tweets:
            f.write(str(time.time()) + "\t" + tweet + "\n")
        f.close()

    def persist_last_status_processed(self, last_status_processed):
        Persister(self.base_dir + self.last_status_processed_file).save(last_status_processed)

    def load_last_status_processed(self):
        return Persister(self.base_dir + self.last_status_processed_file).load()

    def run_scan(self, api, try_count = 0):
        last_status_processed = self.load_last_status_processed()

        if try_count > 10:
            logger.error("Max retries reached")
            return
        try:
            self.scan(api, last_status_processed = last_status_processed)
        except TweepError, e:
            logger.error(e)
        finally:
            time.sleep(30)
            self.run_scan(api, try_count + 1)

