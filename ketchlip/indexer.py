#-*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import re
from ketchlip.sentence import Sentence
import klogger

from persister import Persister
from word import Word

class Indexer:

    # todo refactor links_file to list of links
    def crawl(self, url_list): # returns index, graph of inlinks
        """
        Note that most of the twitter urls are shortened, thus the concept of
        the url (usually shortened) and the expanded url (the response url)

        graph => {url: [list of urls]}
        index => {word: [word_position, url_index_pos]}
        url_lookup => {url_index_pos: [url, expanded_url, title, text]}
        """
        URL_INDEX_POS = 0
        EXPANDED_URL_POS = 1
        TITLE_POS = 2
        TEXT_POS = 3

        crawled = {}
        lookup_url = {} # {url: [expanded url, title, content (100 chars)]}
        graph = {}  # <url>, [list of pages it links to]
        index = {}

        for url in url_list:
            url = url.strip()
            assert len(crawled) == len(lookup_url)

            if url not in crawled:
                content, expanded_url = self.get_page(url)
                if content and expanded_url:
                    crawled[url] = len(crawled.items())
                    lookup_url[url] = [len(lookup_url.items()), "", "", ""]
                    text, title = self.add_page_to_index(index, lookup_url[url][URL_INDEX_POS], content)
                    if text and title:
                        if len(text) > 100:
                            text = text[:100]
                        lookup_url[url][EXPANDED_URL_POS] = expanded_url
                        lookup_url[url][TITLE_POS] = title
                        lookup_url[url][TEXT_POS] = text

                    out_links = self.get_all_links(content)
                    if out_links:
                        graph[url] = out_links
            else:
                klogger.info("Already crawled " + url)


        # reverse the lookup url dictionary

        url_lookup = dict((v[URL_INDEX_POS], [k, v[EXPANDED_URL_POS], v[TITLE_POS], v[TEXT_POS]]) for k, v in lookup_url.iteritems())

        assert len(url_lookup) == len(lookup_url)

        return index, graph, url_lookup

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
        return links

    def union(self, a, b):
        for e in b:
            if e not in a:
                a.append(e)

    def add_page_to_index(self, index, url, content):
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
                return

            words = re.split('\W+', text)

            pos = 0
            for word in words:
                word_list = Word(word).slugify()
                for word in word_list:
                    if word and len(word) > 0 and len(word) < 60:
                        self.add_to_index(index, word, pos, url)
                        pos += 1

            return text, title
        except Exception, e:
            klogger.exception(e)
            return None, None

    def add_to_index(self, index, keyword, pos, url):
        if keyword in index:
            index[keyword].append([pos, url])
        else:
            index[keyword] = [[pos, url]]

# todo rename to tweet_indexer
# todo add blacklist - http://pypi.python.org/pypi/Google%20Safe%20Browsing%20v2%20Lookup/
# todo expand shortened links
# todo put files in config
# todo add title ot short text to url
# todo ignore words ignorewords=set(['the','of','to','and','a','in','is','it'])

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

        index, graph, url_lookup = Indexer().crawl(open(tweetfile, "r"))

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


