from ThreadSafeQueue import ThreadSafeQueue

import time
from threading import Thread

class AudioAnalyzer(Thread):
    def __init__(self, queue: ThreadSafeQueue):
        Thread.__init__(self)
        self.queue = queue
        self.running = False

    def run(self):
        self.running = True

        while self.running:
            frequency = self.queue.pop()
            if frequency is not None:
                print("Dominant frequency:", frequency, "Hz")
            else:
                time.sleep(0.02)

    def stop(self):
        self.running = False
        self.queue.clear()
        self.queue.push(None)