from threading import Lock


class ThreadSafeCounter:
    def __init__(self):
        self._value = 0
        self._lock = Lock()

    def next(self):
        with self._lock:
            self._value += 1
            return self._value


class LogClass:
    Trace = 1
    Info = 2
    Warning = 3
    Exception = 4
