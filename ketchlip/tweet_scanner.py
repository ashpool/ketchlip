#-*- coding: utf-8 -*-

import ConfigParser
import re
import sys
import tweepy
import codecs
from ketchlip import klogger


class CustomStreamListener(tweepy.StreamListener):

    def __init__(self, api=None):
        super(CustomStreamListener, self).__init__(api)
        self.tweets = []

    def get_all_links(self, text):
        links = []
        pattern = r'((https?):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)'
        expression = re.compile(pattern)
        result = expression.findall(text)
        if result:
            for link in result:
                klogger.info("FETCH: " + text)
                links.append(link[0])
        return links

    def on_status(self, status):
        BATCH_SIZE = 10
        try:
            if status.text.find("RT") >= 0:
                # we're not interested in redundant RT spam
                return

            links = self.get_all_links(status.text)
            if len(links) >= 0:
                for link in links:
                    self.tweets.append(link)

                if len(self.tweets) > BATCH_SIZE:
                    klogger.info("Writing tweets to file")
                    f = codecs.open('/tmp/tweets.txt', 'a', 'utf-8')
                    for tweet in self.tweets:
                        f.write(tweet + '\n')
                    f.close()
                    self.tweets = []

        except Exception as e:
            klogger.error('Encountered Exception: ' + str(e))
            pass

    def on_error(self, status_code):
        klogger.error('Encountered error with status code:' +  str(status_code))
        return True # Don't kill the stream

    def on_timeout(self):
        klogger.error('Timeout...')
        return True # Don't kill the stream


def main():
    global streaming_api

    try:
        cfg = ConfigParser.ConfigParser()

        cfg.read("../ketchlip.cfg")
        CONSUMER_KEY=cfg.get('Twitter', 'CONSUMER_KEY')
        CONSUMER_SECRET=cfg.get('Twitter', 'CONSUMER_SECRET')
        ACCESS_TOKEN=cfg.get('Twitter', 'ACCESS_TOKEN')
        ACCESS_TOKEN_SECRET=cfg.get('Twitter', 'ACCESS_TOKEN_SECRET')

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

        api = tweepy.API(auth)

        friends_ids = []
        for friend in tweepy.Cursor(api.friends).items():
            friends_ids.append(friend.id)

        klogger.info(str("Scanning " + api.me().name + " " + str(len(friends_ids))) + " friends")

        csl = CustomStreamListener()
        streaming_api = tweepy.streaming.Stream(auth, csl, timeout=60)
        streaming_api.filter(follow=friends_ids)

    except KeyboardInterrupt:
        klogger.info('^C received, shutting down tweet scanner')
        if streaming_api:
            streaming_api.disconnect()
    except:
        klogger.error("Unexpected error: " + str(sys.exc_info()[0]))

if __name__ == '__main__':
    main()
