from threading import Thread, Event

class RepeatingTimer(Thread):
    def __init__(self, interval_seconds, callback):
        Thread.__init__(self)
        self.stop_event = Event()
        self.interval_seconds = interval_seconds
        self.callback = callback

    def run(self):
        while not self.stop_event.wait(self.interval_seconds):
            self.callback()

    def stop(self):
        self.stop_event.set()