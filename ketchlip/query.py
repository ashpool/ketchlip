#!/usr/bin/env python
# encoding: utf-8

class Query:

    def __init__(self, index):
        self.index =  index



    def multi_lookup(self, query):

        #[['http://c.com', [10]],
        # ['http://a.com', [200]],
        # ['http://d.com', [10]],
        # ['http://b.com', [11, 22, 42]]]
        def quicksort(url_list):
            if not len(url_list):
                return url_list
            # ['http://b.com', [11, 22, 42]
            print url_list[0][1]
            front = quicksort([le for le in url_list[1:] if max(le[1]) - min(le[1])  <= max(url_list[0][1]) - max(url_list[0][1])])
            back = quicksort([gt for gt in url_list[1:] if max(gt[1]) - min(gt[1]) > max(url_list[0][1]) - min(url_list[0][1])])
            return back + [url_list[0]] + front


        WORDPOS = 0
        URL = 1
        urls = {}

        # fetch page candidates
        for word in query:
            if word in self.index:
                candidates = self.index[word]
                for candidate in candidates:
                    if not candidate[URL] in urls:
                        urls[candidate[URL]] = {}
                    if not word in urls[candidate[URL]].keys():
                        urls[candidate[URL]][word] = []
                    urls[candidate[URL]][word].append(candidate[WORDPOS])

        # filter page candidates
        # urls =
        # {'http://c.com': {u'become': [10], u'june': [10]},
        # 'http://a.com': {u'become': [10, 100], u'june': [10]},
        # 'http://d.com': {u'become': [10], u'june': [10]},
        # 'http://b.com': {u'become': [20], u'june': [21]}}
        url_list = []
        for url, words in urls.items():
            if len(words) < len(query):
                continue
            occurences_list = []
            for word, occurences in words.items():
                occurences_list.append(min(occurences))

            url_list.append([url, occurences])
        #[['http://c.com', [10]],
        # ['http://a.com', [200]],
        # ['http://d.com', [10]],
        # ['http://b.com', [11, 22, 42]]]
        sorted_url_list = quicksort(url_list)

        return [li[0] for li in sorted_url_list]