import time
from ketchlip.controllers.base_controller import BaseController
from ketchlip.search_singleton import SearchSingleton
from ketchlip.utils import klogger

class SearchController(BaseController):

    def __init__(self):
        self.name = "search"

    def get_search_singleton(self):
        return SearchSingleton()

    def show(self, query_string):
        query = query_string.get_values("search")
        for i in range(len(query)):
            query[i] = query[i].lower()
        klogger.info("QUERY " + str(query))
        x = time.time()
        results = self.get_search_singleton().query(query)
        search_time_ms = (time.time() - x) * 1000.0
        content = self.get_template().render(query=" ".join(query), results=results, results_len=len(results),
            search_time_in_ms=search_time_ms)
        return content
