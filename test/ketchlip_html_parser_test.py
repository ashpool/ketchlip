#-*- coding: utf-8 -*-
import unittest
from ketchlip.ketchlip_html_parser import KetchlipHTMLParser

class KetchlipHTMLParserTest(unittest.TestCase):

    def setUp(self):

        self.meta = '<meta name="description" content="Nyheter, fördjupning, sportnyheter, ekonominyheter, utrikesnyheter, debatt, ledare, kultur, webb-tv och bloggar. DN.se är utsedd till Sveriges bästa nyhetstidning på nätet./>'

        self.body = \
"""
<body>
    <p>inside a p.</p>
    <table>
        <tr>
            <td>inside a td.</td>
            <td>inside another td.</td>
        <tr>
    </table>
    <div>inside a div.</div>
    <span>inside a span.</div>
</body>
"""
        self.html = \
"""
<html>
    <head>
        <title>This is the title</title>
        <meta name="description" content="This is the content meta tag"/>
    </head>
""" \
+ self.body + \
"""
</html>
"""

        self.html_no_title_text =\
"""
<html>
    <head>
        <title></title>
    </head>
    <body>

    </body>
</html>
"""

        self.html_with_empty_head_and_body =\
"""
<html>
    <head>
    </head>
    <body>

    </body>
</html>
"""
    def test_parse_title(self):
        parser = KetchlipHTMLParser(self.html)
        self.assertEqual("This is the title", parser.title())

    def test_parse_title_should_return_empty_string_if_title_is_empty(self):
        parser = KetchlipHTMLParser(self.html_no_title_text)
        self.assertEqual("", parser.title())

    def test_parse_title_should_return_empty_string_if_title_tag_is_missing(self):
        parser = KetchlipHTMLParser(self.html_with_empty_head_and_body)
        self.assertEqual("", parser.title())

    def test_parse_title_should_return_empty_string_if_content_is_empty(self):
        parser = KetchlipHTMLParser("")
        self.assertEqual("", parser.title())

    def test_parse_text(self):
        parser = KetchlipHTMLParser(self.html)
        self.assertEqual("inside a p. inside a td. inside another td. inside a div. inside a span.", parser.text())

    def test_parse_text_without_body_content_should_return_empty_string(self):
        parser = KetchlipHTMLParser(self.html_with_empty_head_and_body)
        self.assertEqual("", parser.text())

    def test_parse_text_without_empty__html_content_should_return_empty_string(self):
        parser = KetchlipHTMLParser("")
        self.assertEqual("", parser.text())

    def test_parse_description(self):
        parser = KetchlipHTMLParser(self.html)
        self.assertEqual("This is the content meta tag", parser.description())

    def test_parse_description_should_return_empty_string_if_description_is_missing(self):
        parser = KetchlipHTMLParser(self.html_with_empty_head_and_body)
        self.assertEqual("", parser.description())

    def test_parse_description_should_chomp_(self):
        MAX_LENGTH = 20
        parser = KetchlipHTMLParser(self.html)
        self.assertEqual("This is the content ...", parser.description(MAX_LENGTH))


if __name__ == '__main__':
    unittest.main()
