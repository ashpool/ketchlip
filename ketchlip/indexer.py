#-*- coding: utf-8 -*-
from HTMLParser import HTMLParseError
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

# todo Error
"""
2012-05-08 08:55:38,014 - ketchlip.indexer - INFO - All greenlets done
2012-05-08 08:55:38,020 - ketchlip.indexer - INFO - len(self.url_lookup)4016
2012-05-08 08:55:38,021 - ketchlip.indexer - INFO - len(self.lookup_url)4016
2012-05-08 08:55:38,021 - ketchlip.indexer - INFO - Indexing done
2012-05-08 08:55:38,021 - ketchlip.crawler - ERROR -
Traceback (most recent call last):
  File "ketchlip/crawler.py", line 36, in crawl
    url = input_queue.get_nowait()
  File "build/bdist.macosx-10.7-intel/egg/gevent/queue.py", line 204, in get_nowait
    return self.get(False)
  File "build/bdist.macosx-10.7-intel/egg/gevent/queue.py", line 196, in get
    raise Empty
Empty
"""

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
        try:
            logger.info("Starting indexing")
            greenlets = []
            logger.info("Input " + str(not input_queue.empty()))
            logger.info("Result " + str(not result_queue.empty()))

            while not input_queue.empty() or not result_queue.empty():
                if len(greenlets) >= 10:
                    logger.info("Joining indexer greenlets")
                    gevent.joinall(greenlets, timeout=30, raise_error=False)
                    greenlets = []
                    logger.info("Indexers joined")
                    gevent.sleep(0)

                result = result_queue.get(timeout = 10) # the crawlers should be able to produce output below this threshold

                if result[Crawler.STATUS] == "OK":
                    greenlets.append(gevent.spawn(self.indexing, result))

            # make sure to join all little greenlets before continuing
            gevent.joinall(greenlets, timeout=30, raise_error=False)
            logger.info("All greenlets done")

            self.url_lookup = dict((v[self.URL_INDEX_POS], [k, v[self.EXPANDED_URL_POS], v[self.TITLE_POS], v[self.DESCRIPTION_POS]]) for k, v in self.lookup_url.iteritems())
            logger.info("len(self.url_lookup)" + str(len(self.url_lookup)))
            logger.info("len(self.lookup_url)" + str(len(self.lookup_url)))

            assert len(self.url_lookup) == len(self.lookup_url)
            logger.info("Indexing done")

            self.done = True
        except Exception, e:
            self.done = False
            logger.exception(e)


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
            gevent.sleep(0)
        except HTMLParseError, e:
            logger.info("Failed to parse HTML")
        except Exception, e:
            logger.error(e)

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
