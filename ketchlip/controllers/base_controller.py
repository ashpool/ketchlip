from jinja2 import Template

class BaseController():

    def __init__(self):
        self.name = ""

    def show(self, query_string):
        raise NotImplementedError( "Should have implemented this" )

    def get_template(self):
        return Template(self.get_view().show())

    def get_view(self):
        view_name = "".join([self.name[0].upper(), self.name[1:], "View"])
        import_statement = "".join(["from ketchlip.views.", self.name, "_view import ", view_name])
        exec import_statement
        return eval("".join([view_name, "()"]))