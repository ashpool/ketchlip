from BaseHTTPServer import HTTPServer
import ConfigParser
from ketchlip.search_singleton import SearchSingleton
from ketchlip.utils import klogger
from ketchlip.webserver import MyHandler

def main():
    PORT = 80 # you may have to sudo or be su to use port 80
    try:
        klogger.info("Warming up...")

        cfg = ConfigParser.ConfigParser()
        cfg.read("./ketchlip.cfg")

        BASE_DIR = cfg.get("Files", "BASE_DIR")
        WWW_ROOT = cfg.get("Files", "WWW_ROOT")
        MyHandler.set_www_root(WWW_ROOT)

        SearchSingleton().load(BASE_DIR  + "/index", BASE_DIR  + "/url_lookup")
        server = HTTPServer(('', PORT), MyHandler)
        klogger.info("HTTP server ready to serve on port " + str(PORT))
        server.serve_forever()
    except KeyboardInterrupt:
        klogger.info('^C received, shutting down server')
        if server:
            server.socket.close()

if __name__ == '__main__':
    main()