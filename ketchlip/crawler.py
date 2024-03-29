#-*- coding: utf-8 -*-
import urllib2
import gevent
import time
from ketchlip.helpers import klogger

logger = klogger.get_module_logger(__name__)

class Crawler:
    URL = "URL"
    EXPANDED_URL = "EXPANDED_URL"
    TITLE = "TITLE"
    TEXT = "TEXT"
    LINKS = "LINKS"
    CONTENT = "CONTENT"
    STATUS = "STATUS" # OK or FAILED

    def gevent_crawl(self, input_queue, output_queue):
        greenlets = []
        while not input_queue.empty():
            if len(greenlets) >= 10:
                logger.info("Joining crawler greenlets")
                gevent.joinall(greenlets, timeout = 30, raise_error = False)
                greenlets = []
                gevent.sleep(0)

            greenlets.append(gevent.spawn(Crawler().crawl, input_queue, output_queue))

        # make sure to join all greenlets before continuing
        gevent.joinall(greenlets, timeout = 30, raise_error=False)

    def crawl(self, input_queue, output_queue):
        try:
            start = time.time()
            url = input_queue.get(timeout = 10)

            result = {Crawler.URL: url.strip(), Crawler.STATUS: "FAILED"}

            content, expanded_url = self.get_page(url)
            if content and expanded_url:
                result[Crawler.EXPANDED_URL] = expanded_url.strip()
                result[Crawler.CONTENT] = content.strip()
                result[Crawler.STATUS] = "OK"

            if result:
                output_queue.put_nowait(result)
            elapsed = (time.time() - start)
            logger.info("Crawled " + url + " in " + "%.2f" % round(elapsed, 2) + " seconds")
            gevent.sleep(0)
        except Exception, e:
            logger.exception(e)

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
            logger.info(e)
        except Exception, e:
            logger.exception(e)
        return None, None
