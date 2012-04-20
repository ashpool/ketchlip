#-*- coding: utf-8 -*-
from SocketServer import BaseRequestHandler

import cgi
import time
import ConfigParser
import klogger
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from dynamic_content_loader import DynamicContentLoader
from querystring import Querystring
from search_singleton import SearchSingleton
from jinja2 import Template

class MyHandler(BaseHTTPRequestHandler):

    _www_root = 5

    @classmethod
    def get_www_root(cls):
        return cls._www_root

    @classmethod
    def set_www_root(cls, value):
        cls._www_root = value

    def print_beginning(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(\
"""
<html>
    <head>
        <title>Ketchlip</title>
        <link rel="stylesheet" type="text/css" href="/styles/ketchlip.css">
    </head>
    <body>
""")

    def print_end(self):
        self.wfile.write(\
"""
    </body>
</html>
""")

    def do_GET(self):
        try:
            klogger.info("GET " + self.path)

            qs = Querystring(self.path)
            page = qs.page()
            if page:
                query = qs.get_values("search")
                for i in range(len(query)):
                    query[i] = query[i].lower()

                klogger.info("QUERY " + str(query))

                x = time.time()
                results = SearchSingleton().query(query)
                search_time_ms = (time.time() - x) * 1000.0
                template = Template(DynamicContentLoader().load(page))
                content = template.render(query=" ".join(query), results=results, results_len=len(results), search_time_in_ms=search_time_ms)
                self.print_beginning()
                self.wfile.write(content.encode("utf-8"))
                self.print_end()
            elif self.path.endswith(".png"):
                self.send_response(200)
                self.send_header('Content-type',    'image/x-png')
                self.send_header('Cache-control', 'no-cache')
                self.send_header('Pragma', 'no-cache')
                self.end_headers()
                f = open(MyHandler.get_www_root() + self.path)
                self.wfile.write(f.read())
                f.close()
            elif self.path.endswith(".css"):
                print "MyHandler.get_www_root() + self.path", MyHandler.get_www_root() + self.path
                f = open(MyHandler.get_www_root() + self.path)
                self.send_response(200)
                self.send_header('Content-type', 'text/css')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    def do_POST(self):
        global rootnode
        try:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                query=cgi.parse_multipart(self.rfile, pdict)
            self.send_response(301)
            self.end_headers()
            upfilecontent = query.get('upfile')
            self.wfile.write("<HTML>POST OK.<BR><BR>")
            self.wfile.write(upfilecontent[0])
        except:
            pass

def main():
    PORT = 80 # you may have to sudo or be su to use port 80
    try:
        klogger.info("Warming up...")
        # todo load files from config
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

