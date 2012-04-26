#-*- coding: utf-8 -*-

import pickle
import os

class Persister:

    def __init__(self, path):
        self.path = path

    def save(self, data):
        output = open(self.path, 'wb')
        pickle.dump(data, output)
        output.close()

    def load(self, default_return = None):
        data = None
        if os.path.exists(self.path):
            pkl_file = open(self.path, 'rb')
            data = pickle.load(pkl_file)
            pkl_file.close()
        if data:
            return data
        return default_return