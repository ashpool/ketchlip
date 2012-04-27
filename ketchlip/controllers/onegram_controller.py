from operator import itemgetter
from ketchlip.controllers.base_controller import BaseController
from ketchlip.search_singleton import SearchSingleton

class OnegramController(BaseController):

    def __init__(self):
        self.name = "onegram"

    def show(self, query_string):

        index = SearchSingleton().index
        word_count = []

        for k, v in index.items():
            word_count.append([k, len(v)])

        content = self.get_template().render(word_count = sorted(word_count, key=itemgetter(1), reverse=True))
        return content
