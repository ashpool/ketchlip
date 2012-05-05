#-*- coding: utf-8 -*-
import re
import gevent
import time
from crawler import Crawler
from ketchlip.helpers import klogger
from ketchlip.helpers.ketchlip_html_parser import KetchlipHTMLParser
from ketchlip.models.word import Word

logger = klogger.get_module_logger(__name__)

# todo ignore all links on a page
# todo introduce lexicon? {word:word_id}


class Indexer:

    def __init__(self):
        self.URL_INDEX_POS = 0
        self.EXPANDED_URL_POS = 1
        self.TITLE_POS = 2
        self.DESCRIPTION_POS = 3
        self.lookup_url = {} # {url: [expanded url, title, content (100 chars)]}
        self.graph = {}  # <url>, [list of pages it links to]
        self.index = {}
        self.done = False

    def gevent_index(self, input_queue, result_queue):
        greenlets = []
        while not input_queue.empty() or not result_queue.empty():
            if len(greenlets) > 20:
                logger.info("Joining indexer greenlets")
                gevent.joinall(greenlets, timeout=30, raise_error=False)
                greenlets = []

            result = result_queue.get(timeout=15) # the crawlers should be able to produce output below this threshold

            if result[Crawler.STATUS] == "OK":
                greenlets.append(gevent.spawn(Indexer().indexing, result))

        # make sure to join all little greenlets before continuing
        gevent.joinall(greenlets, timeout=30, raise_error=True)
        logger.info("All greenlets done")

        self.url_lookup = dict((v[self.URL_INDEX_POS], [k, v[self.EXPANDED_URL_POS], v[self.TITLE_POS], v[self.DESCRIPTION_POS]]) for k, v in self.lookup_url.iteritems())
        assert len(self.url_lookup) == len(self.lookup_url)
        logger.info("Indexing done")

        self.done = True

    def indexing(self, result):
        """
        result => {Crawler.CONTENT:html, Crawler.URL:http://.., Crawler.EXPANDED_URL:http://.., Crawler.LINKS:[]}
        """
        try:
            start = time.time()
            DESCRIPTION_MAX_LENGTH = 260
            url = result[Crawler.URL].strip()

            if url in self.lookup_url:
                logger.info("Already indexed " + url)
                return

            parser = KetchlipHTMLParser(result[Crawler.CONTENT])
            title = parser.title()
            text = parser.text()
            description = parser.description(DESCRIPTION_MAX_LENGTH)

            self.lookup_url[url] = [len(self.lookup_url.items()), "", "", ""]
            self.lookup_url[url][self.EXPANDED_URL_POS] = result[Crawler.EXPANDED_URL]
            self.lookup_url[url][self.TITLE_POS] = title
            self.lookup_url[url][self.DESCRIPTION_POS] = description
            self.add_page_to_index(self.index, self.lookup_url[url][self.URL_INDEX_POS], " ".join([title, description, text]))

            if Crawler.LINKS in result:
                self.graph[url] = result[Crawler.LINKS]

            elapsed = (time.time() - start)
            logger.info("Indexed " + url + " in " + "%.2f" % round(elapsed, 2) + " seconds")

        except Exception, e:
            logger.exception(e)

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
            logger.exception(e)

    def add_to_index(self, index, keyword, pos, url):
        if keyword in index:
            index[keyword].append([pos, url])
        else:
            index[keyword] = [[pos, url]]
