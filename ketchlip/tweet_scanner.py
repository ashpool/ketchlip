#!/usr/bin/env python
# encoding: utf-8
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
                klogger.info("LINK: " +  link[0] + " TEXT: " + text)
                links.append(link[0])
        return links


    def on_status(self, status):
        try:

            if status.text.find("RT") >= 0:
                klogger.info("PASS: " + status.text)
                return

            links = self.get_all_links(status.text)
            if len(links) >= 0:
                for link in links:
                    self.tweets.append(link)

                if len(self.tweets) > 25:
                    print "printing..."
                    f = codecs.open('/tmp/tweets.txt', 'a', 'utf-8')
                    for tweet in self.tweets:
                        f.write(tweet + '\n')
                    f.close()
                    self.tweets = []
                    print "printing done"
            print "m"
            #print "%s\t%s\t%s\t%s" % (status.text,
            #                          status.author.screen_name,
            #                          status.created_at,
            #                          status.source,)

        except Exception, e:
            print >> sys.stderr, 'Encountered Exception:', e
            pass

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream



# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")

def main():
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

        # If the authentication was successful, you should
        # see the name of the account print out
        print >> sys.stderr, api.me().name

        friends_ids = []
        for friend in tweepy.Cursor(api.friends).items():
            friends_ids.append(friend.id)
        print >> sys.stderr,  len(friends_ids), "friends"
        # Create a streaming API and set a timeout value of 60 seconds.
        csl = CustomStreamListener()
        streaming_api = tweepy.streaming.Stream(auth, csl, timeout=60)

        # Optionally filter the statuses you want to track by providing a list
        # of users to "follow".

        print >> sys.stderr, 'Filtering the public timeline for "%s"' % (' '.join(sys.argv[1:]),)
        streaming_api.filter(follow=friends_ids)

    except KeyboardInterrupt:
        print >> sys.stderr, '^C received, shutting down scanner'
        streaming_api.disconnect()

if __name__ == '__main__':
    main()
