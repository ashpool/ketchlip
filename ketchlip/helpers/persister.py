#-*- coding: utf-8 -*-

try:
    import cPickle as pickle
except:
    import pickle

import gzip

class Persister:

    def __init__(self, path):
        self.path = path

    def save(self, object):
        """
        Serializes an object and store it in a compressed file.
        """
        file = gzip.GzipFile(self.path, 'wb')
        file.write(pickle.dumps(object, 1))
        file.close()

    def load(self, default_return = None):
        """
        Deserializes an object from a compressed file.
        """
        try:
            file = gzip.GzipFile(self.path, 'rb')
            buffer = []
            while True:
                data = file.read()
                if data == "":
                    break
                buffer.append(data)
            object = pickle.loads("".join(buffer))
            file.close()
            if object:
                return object
            return default_return
        except IOError:
            return default_return


