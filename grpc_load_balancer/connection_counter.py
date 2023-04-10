import threading
import logging
class ConnectionCounter:
    def __init__(self, callback):
        self.connected_users = 0
        self.callback = callback
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.connected_users += 1
            if self.callback:
                self.callback(self.connected_users)
            logging.info(f"Connected users: {self.connected_users}")
            

    def decrement(self):
        with self.lock:
            self.connected_users -= 1
            if self.callback:
                self.callback(self.connected_users)

            logging.info(f"Connected users: {self.connected_users}")
