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
    def frequency_to_note_index(frequency):
        A4 = 440
        C0 = A4 * 2 ** (-4.75)
        name = ["C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B"]
        h = round(12 * np.log2(frequency / C0))
        octave = h // 12
        n = h % 12
        return name[n] + str(octave)
    
    def run(self):
        self.running = True

        while self.running:
            frequency = self.queue.pop()
            if frequency is not None:
                self.frequency_to_note_index(frequency)
            else:
                time.sleep(0.01)

    def stop(self):
        self.running = False
        self.queue.clear()
        self.queue.push(None)