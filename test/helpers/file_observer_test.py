import time
from nose.tools import eq_
from ketchlip.helpers.file_observer import FileObserver

class Listener():

    def __init__(self):
        self.message = None
        self.messages = []

    def notify(self, message):
        self.message = message
        self.messages.append(message)

def test_notify():
    file_path = "/tmp/file_path"

    FILE = open(file_path,"w")
    FILE.write("foo")
    FILE.close()

    file_observer = FileObserver(file_path)
    file_observer.POLLING_FREQUENCY_IN_SECONDS = 0
    file_observer.GRACE_TIME_IN_SECONDS = 0
    listener = Listener()

    file_observer.register_listener(listener)
    file_observer.start_observe()
    time.sleep(1)

    FILE = open(file_path,"w")
    FILE.write("bar")
    FILE.close()

    time.sleep(1)
    file_observer.stop_observe()
    eq_("file changed", listener.message)

def test_should_wait_to_notify_until_file_is_closed():

    try:
        # Given a file
        file_path = "/tmp/file_path"

        FILE = open(file_path,"w")
        FILE.write("foo")
        FILE.close()

        # FileObserver will observe file for changes
        file_observer = FileObserver(file_path)
        # For speediness we want to keep the timeouts as short as possible
        file_observer.POLLING_FREQUENCY_IN_SECONDS = 0
        file_observer.GRACE_TIME_IN_SECONDS = 1

        # Listener will get noticed by FileObserver when file is updated
        listener = Listener()
        file_observer.register_listener(listener)
        file_observer.start_observe()
        time.sleep(1)

        # Here we're simulating someone writing to the file
        FILE = open(file_path,"w")
        FILE.write("bar")

        # Assert that the file is still open
        eq_(False, FILE.closed)

        # Sleep and check Listener for messages (should be nothing)
        time.sleep(1)
        eq_(0, len(listener.messages))

        # Close the file and wait till grace time has passed
        FILE.close()
        time.sleep(1)

        # Now the listener should have received an update
        eq_("file changed", listener.message)
        eq_(1, len(listener.messages))

    finally:
        if FILE and not FILE.closed:
            FILE.close()
        if file_observer:
            file_observer.stop_observe()




