#!/usr/bin/env python
# encoding: utf-8

import string,cgi,time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from dynamic_content_loader import DynamicContentLoader
from querystring import Querystring
from search_singleton import SearchSingleton

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            print "GET"
            print "path", self.path
            qs = Querystring(self.path)
            page = qs.page()
            if page:
                self.send_response(200)
                self.send_header('Content-type',	'text/html')
                self.end_headers()

                content = DynamicContentLoader().load(page)
                self.wfile.write(content)
                query = qs.get_values("search")
                for i in range(len(query)):
                    query[i] = query[i].lower()

                print "QUERY", query
                results = SearchSingleton().query(query)
                print "Search result", results
                for url in results:
                    self.wfile.write('<p/>')
                    self.wfile.write('<a href="')
                    self.wfile.write(url)
                    self.wfile.write('" >')
                    self.wfile.write(url)
                    self.wfile.write('</a>')
                return

            return

        except IOError, e:
            self.send_error(404,'File Not Found: %s' % self.path)


    def do_POST(self):
        global rootnode

        try:
            print "POST"
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                query=cgi.parse_multipart(self.rfile, pdict)
            self.send_response(301)

            self.end_headers()
            upfilecontent = query.get('upfile')
            print "filecontent", upfilecontent[0]
            self.wfile.write("<HTML>POST OK.<BR><BR>");
            self.wfile.write(upfilecontent[0]);
        except :
            pass

def main():
    try:
        print "Loading index ..."
        preload = SearchSingleton()
        print "Loading done"
        server = HTTPServer(('', 80), MyHandler)
        print 'started httpserver...'
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()

