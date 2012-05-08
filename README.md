# Ketchlip

I put together Ketchlip to scan Twitter for links in my friends tweets. Ketchlip crawls and indexes links found and
makes them searchable through a simple webserver.


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

> run_tweet_scanner

### Indexing

The script indexer.py reads the tweets.txt produced by tweet_scanner.py and creates and index, graph, and url lookup files.

> run_indexer

### Webserver

The script webserver.py starts a simple http-server that can be accessed on http://localhost/search.twp

> run_webserver

## Testing

Run all tests with coverage report:

> run_tests

## Daemons and Agents on OS X
The .plist files in /osx folder contains daemons for webserver and tweet_scanner and agent ("hourly cron job") for indexer.


## References
* The Anatomy of a Large-Scale Hypertextual Web Search Engine [Sergey Brin, Lawrence Page] http://ilpubs.stanford.edu:8090/361/1/1998-8.pdf

* CS101: Building a Search Engine - Learn key concepts in computer science and build a search engine like google! http://www.udacity.com/overview/Course/cs101/