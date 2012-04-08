#!/usr/bin/env python
# encoding: utf-8

import urllib2
import sys
from bs4 import BeautifulSoup
import re

from persister import Persister
from word import Word


class Indexer:

    def crawl(self, links_file): # returns index, graph of inlinks
        crawled = []
        graph = {}  # <url>, [list of pages it links to]
        index = {}
        file = open(links_file, "r")
        for page in file:
            if page not in crawled:
                content = self.get_page(page)
                if not content:
                    continue
                self.add_page_to_index(index, page, content)
                out_links = self.get_all_links(content)
                if out_links:
                    graph[page] = out_links
                crawled.append(page)
            else:
                print "already crawled %s", page
        file.close()

        return index, graph

    def get_page(self,  url):
        print "opening", url
        try:
            response = urllib2.urlopen(url)
            html = response.read()
            return html
        except Exception, e:
            print >> sys.stderr, 'Encountered Exception:', e
            pass

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
        try:
            soup = BeautifulSoup(content)
            text = soup.get_text()

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
        except Exception, e:
            print >> sys.stderr, 'Encountered Exception:', e
            pass

    def add_to_index(self, index, keyword, pos, url):
        if keyword in index:
            index[keyword].append([pos, url])
        else:
            index[keyword] = [[pos, url]]


def main():
    try:
        index, graph = Indexer().crawl("/tmp/tweets.txt")
        Persister("/tmp/index").save(index)
        Persister("/tmp/graph").save(graph)
    except KeyboardInterrupt:
        print '^C received, shutting down indexer'

if __name__ == '__main__':
    main()


