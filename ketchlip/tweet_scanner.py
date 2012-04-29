#-*- coding: utf-8 -*-

import re
import time
import tweepy
import codecs
from tweepy.error import TweepError
from ketchlip.helpers import klogger
from ketchlip.helpers.persister import Persister

class TweetScanner():
    def get_all_links(self, text):
        links = []
        pattern = r"((https?):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)"
        expression = re.compile(pattern)
        result = expression.findall(text)
        if result:
            for link in result:
                klogger.info("FETCH: " + text)
                links.append(link[0])
        return links

    def scan(self, api, last_status_processed = None, base_dir = "/tmp"):
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
                            klogger.info("Writing tweets to file")
                            f = codecs.open(base_dir + "/tweets.txt", "a", "utf-8")
                            for tweet in tweets:
                                f.write(str(time.time()) + "\t" + tweet + "\n")
                            f.close()
                            Persister(base_dir + "/last_status_processed.txt").save(last_status_processed)
                            tweets = []

            time.sleep(60)

    def run_scan(self, api, last_status_processed, base_dir, try_count = 0):
        if try_count > 10:
            klogger.error("Max retries reached")
            return

        try:
            self.scan(api, last_status_processed = last_status_processed, base_dir = base_dir)
        except TweepError, e:
            klogger.error(e)
        finally:
            time.sleep(30)
            self.run_scan(api, last_status_processed, base_dir, try_count + 1)

