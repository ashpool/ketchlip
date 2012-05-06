from BaseHTTPServer import HTTPServer
from ketchlip.helpers.file_observer import FileObserver
from ketchlip.models.search_singleton import SearchSingleton
from ketchlip.helpers import klogger, config
from ketchlip.webserver import MyHandler

PORT = 80 # you may have to sudo or be su to use port 80


def main():
    try:
        klogger.logger = klogger.get_logger("ketchlip", "webserver.log")

        klogger.info("Starting webserver on port " + str(PORT))

        MyHandler.set_www_root(config.config.www_root)
        index_file, url_lookup_file = config.config.base_dir + "index", config.config.base_dir + "url_lookup"
        SearchSingleton().load(index_file, url_lookup_file)

        file_observer = FileObserver(index_file)
        file_observer.register_listener(SearchSingleton())
        file_observer.start_observe()

        server = HTTPServer(('', PORT), MyHandler)
        klogger.info("HTTP server ready to serve on port " + str(PORT))
        server.serve_forever()
    except KeyboardInterrupt:
        klogger.info('^C received, shutting down server')
        if file_observer:
            file_observer.unregister_listener(SearchSingleton())
            file_observer.stop_observe()
        if server:
            server.socket.close()
    except Exception, e:
        klogger.exception(e)


if __name__ == '__main__':
    main()