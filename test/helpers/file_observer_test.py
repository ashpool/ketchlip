import unittest
import time
from ketchlip.helpers.file_observer import FileObserver


class Listener():
    def notify(self, message):
        self.message = message

class FileObserverTest(unittest.TestCase):

    def test_notify(self):
        file_path = "/tmp/file_path"

        FILE = open(file_path,"w")
        FILE.write("foo")
        FILE.close()

        file_observer = FileObserver(file_path)
        file_observer.TIMEOUT = 0
        listener = Listener()

        file_observer.register_listener(listener)
        file_observer.start_observe()
        time.sleep(1)

        FILE = open(file_path,"w")
        FILE.write("bar")
        FILE.close()

        time.sleep(1)
        file_observer.stop_observe()
        self.assertEqual("file changed", listener.message)

if __name__ == '__main__':
    unittest.main()
