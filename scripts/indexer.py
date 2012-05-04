import gevent
from gevent.queue import Queue
from ketchlip.crawler import Crawler
from ketchlip.indexer import Indexer
from ketchlip.helpers import klogger, config
from ketchlip.helpers.persister import Persister

def main():
    """
    tweet_indexer consumes the output (tweetfile) created by tweet_scanner
    and creates:
    * indexfile: searchable dictionary - {word: [position: url_id]
    * graphfile: each url and their outbound links {url: [list of urls]}
    * url_lookupfile: dictionary containing url ids - {url_id: url}
    """
    try:
        klogger.logger = klogger.get_logger("ketchlip", "indexer.log")

        input_queue = Queue()
        output_queue = Queue()

        base_dir = config.config.base_dir

        tweetfile = base_dir + "tweets.txt" # timestamp \t url
        indexfile = base_dir + "index"
        graphfile = base_dir + "graph"
        url_lookupfile = base_dir + "url_lookup"
        lookup_urlfile = base_dir + "lookup_url"
        since_file = base_dir + "since"

        index_persister = Persister(indexfile)
        graph_persister = Persister(graphfile)
        url_lookup_persister = Persister(url_lookupfile)
        lookup_url_persister = Persister(lookup_urlfile)
        since_persister = Persister(since_file)

        index = index_persister.load({})
        graph = graph_persister.load({})
        lookup_url = lookup_url_persister.load({})
        since = since_persister.load()

        indexer = Indexer()
        indexer.index = index
        indexer.graph = graph
        indexer.lookup_url = lookup_url

        klogger.info("Indexing " + tweetfile)
        if since:
            klogger.info("Since " + str(since))

        url_list = open(tweetfile, "r")
        include_count = 0
        exclude_count = 0
        for timestamp_url in url_list:
            timestamp, url = timestamp_url.split("\t")
            url = url.strip()
            if not url in lookup_url and (not since or since <= timestamp):
                input_queue.put_nowait(url)
                since = timestamp
                include_count += 1
            else:
                exclude_count += 1

        klogger.info("Including: " + str(include_count) + " Excluding: " + str(exclude_count))

        # Spawn off crawler and indexer
        gevent.joinall([
            gevent.spawn(Crawler().gevent_crawl, input_queue, output_queue),
            gevent.spawn_later(10, indexer.gevent_index, input_queue, output_queue)
        ])

        if not indexer.done:
            return klogger.info("Indexing failed")

        index = indexer.index
        graph = indexer.graph
        url_lookup = indexer.url_lookup
        lookup_url = indexer.lookup_url

        index_persister.save(index)
        graph_persister.save(graph)
        url_lookup_persister.save(url_lookup)
        lookup_url_persister.save(lookup_url)
        since_persister.save(since)

        klogger.info("Saved index in " + indexfile + " (length " + str(len(index)) + ")")
        klogger.info("Saved graph in " + graphfile + " (length " + str(len(graph)) + ")")
        klogger.info("Saved lookup url in " + lookup_urlfile + " (length " + str(len(lookup_url)) + ")")
        klogger.info("Saved url lookup in " + url_lookupfile + " (length " + str(len(url_lookup)) + ")")

        klogger.info("Indexing completed")
    except KeyboardInterrupt:
        klogger.info('^C received, shutting down indexer')

if __name__ == '__main__':
    main()
