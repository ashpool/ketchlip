from operator import itemgetter
from ketchlip.controllers.base_controller import BaseController
from ketchlip.models.search_singleton import SearchSingleton

class OnegramController(BaseController):

    def __init__(self):
        self.name = "onegram"

    def show(self, query_string):

        index = SearchSingleton().index
        word_count = []

        for k, v in index.items():
            word_count.append([k, len(v)])

        sorted_word_count = sorted(word_count, key=itemgetter(1), reverse=True)

        content = self.get_template().render(load_time = SearchSingleton().load_time, number_of_words = len(index), number_of_pages = len(SearchSingleton().url_lookup), top_100 = sorted_word_count[:100])
        return content
