import unittest
from bs4 import BeautifulSoup
from ketchlip.controllers.search_controller import SearchController
from ketchlip.models.querystring import Querystring


class SearchControllerTest(unittest.TestCase):
    def test_show(self):
        qs = Querystring("http://localhost/search?search=hello+world")
        soup = BeautifulSoup(SearchControllerStub().show(qs))
        self.assertEqual("Ketchlip", soup.head.title.get_text())


class SearchControllerStub(SearchController):
    def get_search_singleton(self):
        return SearchSingletonStub()

class SearchSingletonStub():
    def query(self, query):
        return []