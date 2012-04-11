#-*- coding: utf-8 -*-
import ConfigParser
import re
import time
import tweepy
import codecs
from ketchlip import klogger
from ketchlip.persister import Persister


def get_all_links(text):
    links = []
    pattern = r'((https?):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)'
    expression = re.compile(pattern)
    result = expression.findall(text)
    if result:
        for link in result:
            klogger.info("FETCH: " + text)
            links.append(link[0])
    return links

def scan(api, last_status_processed = None):
    BATCH_SIZE = 5
    tweets = []

    while True:
        for status in tweepy.Cursor(api.friends_timeline, since_id=last_status_processed).items(20):
            if last_status_processed is None:
                last_status_processed = status.id
                break

            if status.id > last_status_processed:
                last_status_processed = status.id

            links = get_all_links(status.text)

            if len(links) >= 0:
                for link in links:
                    tweets.append(link)

                    if len(tweets) > BATCH_SIZE:
                        klogger.info("Writing tweets to file")
                        f = codecs.open('/tmp/tweets.txt', 'a', 'utf-8')
                        for tweet in tweets:
                            f.write(tweet + '\n')
                        f.close()
                        Persister("/tmp/last_status_processed.txt").save(last_status_processed)
                        tweets = []

        time.sleep(60)

def main():
    try:
        cfg = ConfigParser.ConfigParser()

        cfg.read("../ketchlip.cfg")
        CONSUMER_KEY = cfg.get('Twitter', 'CONSUMER_KEY')
        CONSUMER_SECRET = cfg.get('Twitter', 'CONSUMER_SECRET')
        ACCESS_TOKEN = cfg.get('Twitter', 'ACCESS_TOKEN')
        ACCESS_TOKEN_SECRET = cfg.get('Twitter', 'ACCESS_TOKEN_SECRET')

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        api = tweepy.API(auth)

        klogger.info(str("Scanning " + api.me().name + " friends timeline"))
        last_status_processed = Persister("/tmp/last_status_processed.txt").load()
        scan(api, last_status_processed = last_status_processed)
    except KeyboardInterrupt:
        klogger.info('^C received, shutting down tweet scanner')


if __name__ == '__main__':
    main()
