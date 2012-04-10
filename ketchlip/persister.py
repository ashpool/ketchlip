#-*- coding: utf-8 -*-

import pickle

class Persister:

    def __init__(self, path):
        self.path = path

    def save(self, data):
        # write python dict to a file
        output = open(self.path, 'wb')
        pickle.dump(data, output)
        output.close()

    def load(self):
        # read python dict back from the file
        pkl_file = open(self.path, 'rb')
        data = pickle.load(pkl_file)
        pkl_file.close()
        return data