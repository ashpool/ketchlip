# Ketchlip

Inspired by the Udacity cs101 course I put together Ketchlip to scan Twitter for links in my friends tweets. 
Ketchlip then crawl and index links found and makes them searchable through a simple webserver. I'm doing this for fun!


## Dependencies

Ketchlip needs these libraries to run:
> pip install 'library name'

* tweepy
* nose
* mock
* BeautifulSoup4
* pickle
* jinja2
* gevent

## Usage

### Scanning
The script tweet_scanner.py will scan your friends timeline for links in tweets. Links found are saved in /tmp/tweets.txt.
You will need to configure your Twitter access tokens in ketchlip.cfg in order to connect with Twitter.
The access tokens can be found on your applications's Details page located at https://dev.twitter.com/apps
(located under "Your access token"). tweet_scanner will save the last loaded status id, so when the script is run later it
will catch up from last status to current in the timeline.

> python tweet_scanner.py

or

> run_tweet_scanner

### Indexing

The script indexer.py reads the tweets.txt produced by tweet_scanner.py and creates and index, graph, and url lookup files.

> python indexer.py

or

> run_indexer

### Webserver

The script webserver.py starts a simple http-server that can be accessed on http://localhost/search.twp

> python webserver.py

or

> run_webserver

## Testing

Run all tests with coverage report:

> nosetests --quiet --with-coverage --cover-package ketchlip

or

> run_tests


