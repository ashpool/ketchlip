class ControllerFactory():

    def create(self, name):
        controller_name = name[0].upper() + name[1:] + "Controller"
        exec "".join(["from controllers.", name, "_controller import ", controller_name])
        return eval("".join([controller_name, "()"]))