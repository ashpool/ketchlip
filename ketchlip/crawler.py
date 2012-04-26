#-*- coding: utf-8 -*-
import urllib2
import gevent
import time
from ketchlip.utils import klogger


class Crawler:
    URL = "URL"
    EXPANDED_URL = "EXPANDED_URL"
    TITLE = "TITLE"
    TEXT = "TEXT"
    LINKS = "LINKS"
    CONTENT = "CONTENT"
    STATUS = "STATUS" # OK or FAILED

    def gevent_crawl(self, input_queue, output_queue, name):
        while not input_queue.empty():
            start = time.time()
            url = input_queue.get_nowait()

            gevent.sleep(0)
            result = self.crawl(url)
            if result:
                output_queue.put_nowait(result)
            elapsed = (time.time() - start)
            klogger.info("Crawler " + name + " crawled " + url + " in " + str(elapsed) + " seconds")

    def crawl(self, url):
        result = {Crawler.URL: url.strip(), Crawler.STATUS: "FAILED"}

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
            response = urllib2.urlopen(url) # this is blocking, probably http://t.co/ does not allow more than one browser
            html = response.read()
            expanded_url = response.url

            return html, expanded_url
        except urllib2.HTTPError, e:
            klogger.info(e)
        except Exception, e:
            klogger.exception(e)
        return None, None
