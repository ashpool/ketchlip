#-*- coding: utf-8 -*-
import ConfigParser
from HTMLParser import HTMLParseError
import urllib2
import re
import gevent
from gevent.queue import Queue
import time
from ketchlip_html_parser import KetchlipHTMLParser
import klogger

from persister import Persister
from word import Word

class Crawler:
    URL = "URL"
    EXPANDED_URL = "EXPANDED_URL"
    TITLE = "TITLE"
    TEXT = "TEXT"
    LINKS = "LINKS"
    CONTENT = "CONTENT"
    STATUS = "STATUS" # OK or FAILED

    # todo something seems to block the crawler - does http://t.co/ allow more than one browser or is the fault here?
    def gevent_crawl(self, name):
        while not input_queue.empty():
            start = time.time()
            url = input_queue.get()

            gevent.sleep(0)
            result = self.crawl(url)
            if result:
                output_queue.put_nowait(result)
            elapsed = (time.time() - start)
            klogger.info("Crawler " + name + " crawled " + url + " in " + str(elapsed) + " seconds")

    def crawl(self, url):
        result = {}
        result[Crawler.URL] = url.strip()
        result[Crawler.STATUS] = "FAILED"  # let's start out with some pessimism ;-)

        content, expanded_url = self.get_page(url)
        if content and expanded_url:
            result[Crawler.EXPANDED_URL] = expanded_url.strip()
            result[Crawler.CONTENT] = content.strip()
            result[Crawler.STATUS] = "OK"

        return result


    def get_page(self,  url):
        """
        Opens the url and return its content and expanded url.
        """
        try:
            response = urllib2.urlopen(url)
            html = response.read()
            expanded_url = response.url

            return html, expanded_url
        except urllib2.HTTPError, e:
            klogger.info(e)
        except Exception, e:
            klogger.exception(e)
        return None, None

class Indexer:

    def __init__(self):
        #self.ignorewords=set(['the','of','to','and','a','in','is','it'])
        self.URL_INDEX_POS = 0
        self.EXPANDED_URL_POS = 1
        self.TITLE_POS = 2
        self.TEXT_POS = 3


        self.lookup_url = {} # {url: [expanded url, title, content (100 chars)]}
        self.graph = {}  # <url>, [list of pages it links to]
        self.index = {}

    def gevent_index(self, input_queue, result_queue):
        self.done = False

        gevent.sleep(30) # give the crawlers some heads up

        while not (input_queue.empty() and result_queue.empty()):
            result = result_queue.get(timeout=15) # the crawlers should be able to produce output below this threshold
            if result[Crawler.STATUS] == "OK":
                self.indexing(result)
            gevent.sleep(0)

        self.url_lookup = dict((v[self.URL_INDEX_POS], [k, v[self.EXPANDED_URL_POS], v[self.TITLE_POS], v[self.TEXT_POS]]) for k, v in self.lookup_url.iteritems())
        assert len(self.url_lookup) == len(self.lookup_url)
        self.done = True

    def indexing(self, result):
        try:
            url = result[Crawler.URL].strip()

            if url in self.lookup_url:
                klogger.info("Already crawled " + url)
                return
            klogger.info("Indexing " + url)

            parser = KetchlipHTMLParser(result[Crawler.CONTENT])
            title = parser.title()
            text = parser.text()
            short_text = text
            if len(short_text) > 100:
                short_text = short_text[:100]

            self.lookup_url[url] = [len(self.lookup_url.items()), "", "", ""]
            self.lookup_url[url][self.EXPANDED_URL_POS] = result[Crawler.EXPANDED_URL]
            self.lookup_url[url][self.TITLE_POS] = title
            self.lookup_url[url][self.TEXT_POS] = short_text
            self.add_page_to_index(self.index, self.lookup_url[url][self.URL_INDEX_POS], text)

            if Crawler.LINKS in result:
                self.graph[url] = result[Crawler.LINKS]
        except HTMLParseError, e:
            klogger.info(e)

        except Exception, e:
            klogger.error(e)

    def add_page_to_index(self, index, url, content):
        """
        Splits the content of the url and adds every single word and its position to the index.
        """
        try:
            words = re.split('\W+', content)

            pos = 0
            for word in words:
                word_list = Word(word).slugify()
                for word in word_list:
                    if word and len(word) > 0 and len(word) < 60:
                        self.add_to_index(index, word, pos, url)
                        pos += 1

        except Exception, e:
            klogger.exception(e)


    def add_to_index(self, index, keyword, pos, url):
        if keyword in index:
            index[keyword].append([pos, url])
        else:
            index[keyword] = [[pos, url]]

input_queue = Queue()
output_queue = Queue()

# todo refactor this
def main():
    """
    tweet_indexer consumes the output (tweetfile) created by tweet_scanner
    and creates:
    * indexfile: searchable dictionary - {word: [position: url_id]
    * graphfile: each url and their outbound links {url: [list of urls]}
    * url_lookupfile: dictionary containing url ids - {url_id: url}
    """
    try:
        cfg = ConfigParser.ConfigParser()
        cfg.read("./ketchlip.cfg")

        BASE_DIR = cfg.get("Files", "BASE_DIR")

        tweetfile = BASE_DIR + "/tweets.txt" # timestamp \t url
        indexfile = BASE_DIR + "/index"
        graphfile = BASE_DIR + "/graph"
        url_lookupfile = BASE_DIR + "/url_lookup"
        lookup_urlfile = BASE_DIR + "/lookup_url"
        since_file = BASE_DIR + "/since"

        index_persister = Persister(indexfile)
        graph_persister = Persister(graphfile)
        url_lookup_persister = Persister(url_lookupfile)
        lookup_url_persister = Persister(lookup_urlfile)
        since_persister = Persister(since_file)

        index = index_persister.load({})
        graph = graph_persister.load({})
        lookup_url = lookup_url_persister.load({})
        since = since_persister.load()

        indexer = Indexer()
        indexer.index = index
        indexer.graph = graph
        indexer.lookup_url = lookup_url

        klogger.info("Indexing " + tweetfile)
        if since:
            klogger.info("Since " + str(since))

        url_list = open(tweetfile, "r")
        for timestamp_url in url_list:
            timestamp, url = timestamp_url.split("\t")
            url = url.strip()
            if not url in lookup_url and (not since or since <= timestamp):
                input_queue.put_nowait(url)
                klogger.info("Including " + url)
                since = timestamp
            else:
                klogger.info("Excluding " + url)

        # Spawn off multiple crawlers and one indexer
        gevent.joinall([
            gevent.spawn(Crawler().gevent_crawl, "A"),
            gevent.spawn(Crawler().gevent_crawl, "B"),
            gevent.spawn(Crawler().gevent_crawl, "C"),
            gevent.spawn(Crawler().gevent_crawl, "D"),
            gevent.spawn(Crawler().gevent_crawl, "E"),
            gevent.spawn(indexer.gevent_index, input_queue, output_queue)
            ])

        if not indexer.done:
            return klogger.info("Indexing failed")

        index = indexer.index
        graph = indexer.graph
        url_lookup = indexer.url_lookup
        lookup_url = indexer.lookup_url

        index_persister.save(index)
        graph_persister.save(graph)
        url_lookup_persister.save(url_lookup)
        lookup_url_persister.save(lookup_url)
        since_persister.save(since)

        klogger.info("Saved index in " + indexfile + " (length " + str(len(index)) + ")")
        klogger.info("Saved graph in " + graphfile + " (length " + str(len(graph)) + ")")
        klogger.info("Saved lookup url in " + lookup_urlfile + " (length " + str(len(lookup_url)) + ")")
        klogger.info("Saved url lookup in " + url_lookupfile + " (length " + str(len(url_lookup)) + ")")

        klogger.info("Indexing completed")
    except KeyboardInterrupt:
        klogger.info('^C received, shutting down indexer')

if __name__ == '__main__':
    main()

