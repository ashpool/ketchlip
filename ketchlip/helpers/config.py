class Config():

    def __init__(self, params = {}):
        for k, v in params.items():
            setattr(self, k, v)