#-*- coding: utf-8 -*-

import cgi
import time
import klogger
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from dynamic_content_loader import DynamicContentLoader
from querystring import Querystring
from search_singleton import SearchSingleton
from jinja2 import Template

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            klogger.info("GET " + self.path)

            qs = Querystring(self.path)
            page = qs.page()
            if page:
                self.send_response(200)
                self.send_header('Content-type',	'text/html')
                self.end_headers()

                query = qs.get_values("search")
                for i in range(len(query)):
                    query[i] = query[i].lower()

                klogger.info("QUERY " + str(query))

                x = time.time()
                results = SearchSingleton().query(query)
                search_time_ms = (time.time() - x) * 1000.0

                template = Template(DynamicContentLoader().load(page))
                content = template.render(query=" ".join(query), results=results, results_len=len(results), search_time_in_ms=search_time_ms)
                self.wfile.write(content)
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
    PORT = 80
    try:
        klogger.info("Warming up...")
        SearchSingleton().load("/tmp/index", "/tmp/url_lookup")
        server = HTTPServer(('', PORT), MyHandler)
        klogger.info("HTTP server ready to serve on port " + str(PORT))
        server.serve_forever()
    except KeyboardInterrupt:
        klogger.info('^C received, shutting down server')
        if server:
            server.socket.close()

if __name__ == '__main__':
    main()

