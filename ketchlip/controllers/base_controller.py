from jinja2 import Template
from ketchlip.dynamic_content_loader import DynamicContentLoader

class BaseController():

    def show(self, query_string):
        raise NotImplementedError( "Should have implemented this" )

    def get_template(self):
        return Template(DynamicContentLoader().load(self.name + ".twp"))
