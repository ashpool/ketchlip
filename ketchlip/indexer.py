#-*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import re
import gevent
from gevent.queue import Queue
from ketchlip.sentence import Sentence
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

    def gevent_crawl(self, name):
        while not input_queue.empty():
            url = input_queue.get()
            print "Crawler", name, "received",  url
            gevent.sleep(0)
            result = self.crawl(url)
            if result:
                output_queue.put_nowait(result)

    def crawl(self, url):
        content, expanded_url = self.get_page(url)
        if content and expanded_url:
            text, title = self.parse_page(content)
            if text and title:
                if len(text) > 100:
                    text = text[:100]
                result = {}
                result[Crawler.URL] = url.strip()
                result[Crawler.EXPANDED_URL] = expanded_url.strip()
                result[Crawler.TITLE] = title.strip()
                result[Crawler.TEXT] = text.strip()
                result[Crawler.CONTENT] = content.strip()

                return result


    def get_page(self,  url):
        """
        Opens the url and return its content and expanded url.
        """
        try:
            response = urllib2.urlopen(url)
            html = response.read()
            expanded_url = response.url

            klogger.info("Opened " +  expanded_url)

            return html, expanded_url
        except Exception, e:
            klogger.exception(e)
            return None, None

    def parse_page(self, content):
        """
        Splits the content of the url and adds every single word and its position to the index.
        """
        try:
            # todo BeautifulSoup is throwing a lots of errors - too sensitive to malformatted html?
            soup = BeautifulSoup(content)
            text = soup.html.body.get_text()
            title = ""
            if soup.html and soup.html.head and soup.html.title:
                title = Sentence(soup.html.head.title.string).sanitize()

            if not text:
                return None, None

            return text, title
        except Exception, e:
            klogger.exception(e)
            return None, None

    def get_next_target(self, page):
        start_link = page.find('<a href=')
        if start_link == -1:
            return None, 0
        start_quote = page.find('"', start_link)
        end_quote = page.find('"', start_quote + 1)
        url = page[start_quote + 1:end_quote]
        return url, end_quote

    def get_all_links(self, page):
        links = []
        while True:
            url, end_pos = self.get_next_target(page)
            if url:
                links.append(url)
                page = page[end_pos:]
            else:
                break

class Indexer:

    def index(self, results):
        crawled = {}
        lookup_url = {} # {url: [expanded url, title, content (100 chars)]}
        graph = {}  # <url>, [list of pages it links to]
        index = {}

        for result in results:
            URL_INDEX_POS = 0
            EXPANDED_URL_POS = 1
            TITLE_POS = 2
            TEXT_POS = 3

            url = result[Crawler.URL]
            assert len(crawled) == len(lookup_url)

            if url in crawled:
                klogger.info("Already crawled " + url)
                return


            crawled[url] = len(crawled.items())
            lookup_url[url] = [len(lookup_url.items()), "", "", ""]

            lookup_url[url][EXPANDED_URL_POS] = result[Crawler.EXPANDED_URL]
            lookup_url[url][TITLE_POS] = result[Crawler.TITLE]
            lookup_url[url][TEXT_POS] = result[Crawler.TEXT]
            self.add_page_to_index(index, lookup_url[url][URL_INDEX_POS], result[Crawler.CONTENT])

            if Crawler.LINKS in result:
                graph[url] = result[Crawler.LINKS]

        url_lookup = dict((v[URL_INDEX_POS], [k, v[EXPANDED_URL_POS], v[TITLE_POS], v[TEXT_POS]]) for k, v in lookup_url.iteritems())
        assert len(url_lookup) == len(lookup_url)

        return index, graph, url_lookup


    def add_page_to_index(self, index, url, content):
        """
        Splits the content of the url and adds every single word and its position to the index.
        """
        try:
            # todo BeautifulSoup is throwing a lots of errors - too sensitive to malformatted html?
            soup = BeautifulSoup(content)
            text = soup.html.body.get_text()

            words = re.split('\W+', text)

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

# todo make indexer continue on old index file
# todo put files in config
# todo ignore words ignorewords=set(['the','of','to','and','a','in','is','it'])

input_queue = Queue()
output_queue = Queue()

def main():
    """
    tweet_indexer consumes the output (tweetfile) created by tweet_scanner
    and creates:
    * indexfile: searchable dictionary - {word: [position: url_id]
    * graphfile: each url and their outbound links {url: [list of urls]}
    * url_lookupfile: dictionary containing url ids - {url_id: url}
    """
    try:
        tweetfile = "/tmp/tweets.txt"
        indexfile = "/tmp/index"
        graphfile = "/tmp/graph"
        url_lookupfile = "/tmp/url_lookup"

        klogger.info("Indexing " + tweetfile)

        url_list = open(tweetfile, "r")
        for url in url_list:
            input_queue.put_nowait(url)

        # Spawn off multiple crawlers
        gevent.joinall([
            gevent.spawn(Crawler().gevent_crawl, "foo"),
            gevent.spawn(Crawler().gevent_crawl, "bar"),
            gevent.spawn(Crawler().gevent_crawl, "zoz"),
            gevent.spawn(Crawler().gevent_crawl, "zap"),
            gevent.spawn(Crawler().gevent_crawl, "fuz")
            ])

        results = []
        while not output_queue.empty():
            results.append(output_queue.get())
            gevent.sleep(0)

        index, graph, url_lookup = Indexer().index(results)

        Persister(indexfile).save(index)
        Persister(graphfile).save(graph)
        Persister(url_lookupfile).save(url_lookup)

        klogger.info("Saved index in " + indexfile + " (length " + str(len(index)) + ")")
        klogger.info("Saved graph in " + graphfile + " (length " + str(len(graph)) + ")")
        klogger.info("Saved lookup in " + url_lookupfile + " (length " + str(len(url_lookup)) + ")")

        klogger.info("Indexing completed")
    except KeyboardInterrupt:
        klogger.info('^C received, shutting down indexer')

if __name__ == '__main__':
    main()
