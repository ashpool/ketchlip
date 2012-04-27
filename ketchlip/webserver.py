#-*- coding: utf-8 -*-

from controller_factory import ControllerFactory
from BaseHTTPServer import BaseHTTPRequestHandler
from utils import klogger
from querystring import Querystring

class MyHandler(BaseHTTPRequestHandler):

    _www_root = 5

    @classmethod
    def get_www_root(cls):
        return cls._www_root

    @classmethod
    def set_www_root(cls, value):
        cls._www_root = value

    def write_js(self):
        f = open(MyHandler.get_www_root() + self.path)
        self.send_response(200)
        self.send_header('Content-type', 'text/javascript')
        self.end_headers()
        self.wfile.write(f.read())
        f.close()

    def write_css(self):
        f = open(MyHandler.get_www_root() + self.path)
        self.send_response(200)
        self.send_header('Content-type', 'text/css')
        self.end_headers()
        self.wfile.write(f.read())
        f.close()

    def write_png(self):
        self.send_response(200)
        self.send_header('Content-type', 'image/x-png')
        self.send_header('Cache-control', 'no-cache')
        self.send_header('Pragma', 'no-cache')
        self.end_headers()
        f = open(MyHandler.get_www_root() + self.path)
        self.wfile.write(f.read())
        f.close()

    def write_page(self, page, qs):

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        controller = ControllerFactory().create(page.split(".")[0])
        content = controller.show(qs)

        self.wfile.write(content.encode("utf-8"))

    def do_GET(self):
        try:
            klogger.info("GET " + self.path)

            qs = Querystring(self.path)
            page = qs.page()
            if self.path.endswith(".png"):
                self.write_png()
            elif self.path.endswith(".css"):
                self.write_css()
            elif self.path.endswith(".js"):
                self.write_js()
            elif page:
                self.write_page(page, qs)

            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

# Not used for now
#
#    def do_POST(self):
#        global rootnode
#        try:
#            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
#            if ctype == 'multipart/form-data':
#                query=cgi.parse_multipart(self.rfile, pdict)
#            self.send_response(301)
#            self.end_headers()
#            upfilecontent = query.get('upfile')
#            self.wfile.write("<HTML>POST OK.<BR><BR>")
#            self.wfile.write(upfilecontent[0])
#        except:
#            pass


