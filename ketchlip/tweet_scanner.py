#-*- coding: utf-8 -*-
import ConfigParser
import re
import time
import tweepy
import codecs
from ketchlip import klogger

def process_text(text, tweets):
    BATCH_SIZE = 5 # todo is BATCH_SIZE really needed?
    try:
        links = get_all_links(text)
        if len(links) >= 0:
            for link in links:
                tweets.append(link)

            if len(tweets) > BATCH_SIZE:
                klogger.info("Writing tweets to file")
                f = codecs.open('/tmp/tweets.txt', 'a', 'utf-8')
                for tweet in tweets:
                    f.write(tweet + '\n')
                f.close()
                tweets = []
        return tweets

    except Exception as e:
        klogger.error('Encountered Exception: ' + str(e))
        return tweets


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


lastStatusProcessed = None

def scan(api):
    lastStatusProcessed = None

    tweets = []

    while True:
        for status in tweepy.Cursor(api.friends_timeline, since_id=lastStatusProcessed).items(20):
            if lastStatusProcessed is None:
                lastStatusProcessed = status.id
                break

            if status.id > lastStatusProcessed:
                lastStatusProcessed = status.id

            tweets = process_text(status.text, tweets)

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

        scan(api)
    except KeyboardInterrupt:
        klogger.info('^C received, shutting down tweet scanner')
        print "lastStatusProcessed", lastStatusProcessed

    except Exception, e:
        klogger(e)

if __name__ == '__main__':
    main()
