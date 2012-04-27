import unittest
from ketchlip.controller_factory import ControllerFactory
from ketchlip.controllers.search_controller import SearchController

class ControllerFactoryTest(unittest.TestCase):

    def test_get_search_controller(self):
        self.assertIsInstance(ControllerFactory().create("search"), SearchController)

if __name__ == '__main__':
    unittest.main()
