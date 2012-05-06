#-*- coding: utf-8 -*-
import shutil

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

        Pickling large objects can take a long time, so as
        a safety measure, the file is written to a temporary file
        and when done, it is moved to 'path'.
        """
        temp_path = self.path + "_tmp"
        file = gzip.GzipFile(temp_path, 'wb')
        file.write(pickle.dumps(object,  protocol=2))
        file.close()
        shutil.move(temp_path, self.path)

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


