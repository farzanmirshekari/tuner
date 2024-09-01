from ThreadSafeQueue import ThreadSafeQueue

import numpy as np

from threading import Thread
import time

class InstrumentTuner(Thread):

    def __init__(self, queue: ThreadSafeQueue):
        Thread.__init__(self)
        self.queue = queue
        self.running = False

    @staticmethod
    def frequency_to_note(frequency):
        A4 = 440
        C0 = A4 * 2 ** (-4.75)
        name = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        h = round(12 * np.log2(frequency / C0))
        octave = h // 12
        n = h % 12
        return name[n] + str(octave)
    
    def run(self):
        self.running = True

        while self.running:
            frequency = self.queue.pop()
            if frequency is not None and frequency > 0:
                self.frequency_to_note(frequency)
            else:
                time.sleep(0.5)

    def stop(self):
        self.running = False
        self.queue.clear()
        self.queue.push(None)