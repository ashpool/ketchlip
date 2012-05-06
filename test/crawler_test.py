from Queue import Queue
import urllib2
from mock import Mock
from nose.tools import eq_
from ketchlip.crawler import Crawler

def test_crawl():
    html =\
    """<html>
        <head>
            <title>Python is fun!</title>
        </head>
        <body>
            <div>Python is similar to Ruby, but different.</div>
        </body>
    </html>"""

    response_mock = Mock(url="http://expanded_url.com")
    response_mock.read = Mock(return_value=html)
    urllib2.urlopen = Mock(return_value=response_mock)
    url = "http://a.com"

    input_queue = Mock()
    input_queue.get_nowait = Mock(return_value=url)
    output_queue = Queue()

    crawler = Crawler()

    crawler.crawl(input_queue, output_queue)

    expected_result = {'CONTENT': html,
                       'EXPANDED_URL': 'http://expanded_url.com',
                       'STATUS': 'OK',
                       'URL': 'http://a.com'}

    eq_(expected_result, output_queue.get())

