#-*- coding: utf-8 -*-
import os
from threading import Thread
import gevent
import time

class FileObserver():
    def __init__(self, file_path):
        self.listeners = []
        self.file_path = file_path
        self.last_st_mtime = 0
        self.run = True
        self.TIMEOUT = 30

    def start_observe(self):
        self.t = Thread(target=self.observe)
        self.t.start()

    def stop_observe(self):
        if self.t and self.t.is_alive():
            self.run = False
            self.t.join()

    def observe(self):
        while self.run:
            st_mtime = os.stat(self.file_path).st_mtime
            if st_mtime > self.last_st_mtime:
                self.notify_listeners("file changed")
                self.last_st_mtime = st_mtime
            time.sleep(self.TIMEOUT)

    def register_listener(self, observer):
        self.listeners.append(observer)

    def unregister_listener(self, observer):
        if observer in self.listeners:
            self.listeners.remove(observer)

    def notify_listeners(self, message):
        greenlets = []
        for listener in self.listeners:
            greenlets.append(gevent.spawn(listener.notify, message))
        gevent.joinall(greenlets)