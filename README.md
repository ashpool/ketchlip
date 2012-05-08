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

## Ideas and Open Questions

Single word searches now: First occurence of a the search word wins.
Multi word searches now: Minimum distance between min and max word in search phrase wins.

Alternatively, how should:
* number of occurances affect search result?
* places of occurance affect search result (title/description/links/body)

Would a reverse index ({page: list of word positions}) help?

What to do with common words like "the", "of", "a" etc?

Search options
The Google operators:
* OR – Search for either one, such as "price high OR low" searches for "price" with "high" or "low".
* "-" – Search while excluding a word, such as "apple -tree" searches where word "tree" is not used.

Some query options:
site: – Restrict the results to those websites in the given domain,[28] such as, site:www.acmeacme.com. The option "site:com" will search all domain URLs named with ".com" (no space after "site:").
allintitle: – Only the page titles are searched (not the remaining text on each webpage).
intitle: – Prefix to search in a webpage title, such as "intitle:google search" will list pages with word "google" in title, and word "search" anywhere (no space after "intitle:").
allinurl: – Only the page URL address lines are searched (not the text inside each webpage).
inurl: – Prefix for each word to be found in the URL; others words are matched anywhere, such as "inurl:acme search" matches "acme" in a URL, but matches "search" anywhere (no space after "inurl:").


## References
* The Anatomy of a Large-Scale Hypertextual Web Search Engine [Sergey Brin, Lawrence Page] http://ilpubs.stanford.edu:8090/361/1/1998-8.pdf

* CS101: Building a Search Engine - Learn key concepts in computer science and build a search engine like google! http://www.udacity.com/overview/Course/cs101/