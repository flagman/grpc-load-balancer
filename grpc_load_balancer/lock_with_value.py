import threading

class LockWithValue:
    def __init__(self):
        self.value = False
        self.lock = threading.Lock()