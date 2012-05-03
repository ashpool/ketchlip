from BaseHTTPServer import HTTPServer
import ConfigParser
from ketchlip.models.search_singleton import SearchSingleton
from ketchlip.helpers import klogger, config
from ketchlip.webserver import MyHandler

def main():
    PORT = 80 # you may have to sudo or be su to use port 80
    try:
        klogger.info("Warming up...")

        MyHandler.set_www_root(config.config.www_root)

        SearchSingleton().load(config.config.base_dir + "index", config.config.base_dir + "url_lookup")
        server = HTTPServer(('', PORT), MyHandler)
        klogger.info("HTTP server ready to serve on port " + str(PORT))
        server.serve_forever()
    except KeyboardInterrupt:
        klogger.info('^C received, shutting down server')
        if server:
            server.socket.close()

if __name__ == '__main__':
    main()