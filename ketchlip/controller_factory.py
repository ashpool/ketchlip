class ControllerFactory():

    def create(self, name):
        controller_name = name[0].upper() + name[1:] + "Controller"
        import_statement = "from controllers." + name + "_controller import " + controller_name
        exec import_statement
        return eval(controller_name + "()")