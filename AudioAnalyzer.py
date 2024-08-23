from threading import Thread

from ThreadSafeQueue import ThreadSafeQueue

class AudioAnalyzer(Thread):

    def __init__(self, queue: ThreadSafeQueue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            if not self.queue.size() == 0:
                frequency = self.queue.pop()
                print("Dominant Frequency: ", frequency, "Hz")

    def stop(self):
        self.queue.queue.clear()
        self.queue.queue.append(None)