from ThreadSafeQueue import ThreadSafeQueue

import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal

import time

class InstrumentTuner(QThread):

    frequency_detected = pyqtSignal(float)

    NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    A4 = 440
    C0 = A4 * 2 ** (-4.75)

    def __init__(self, queue: ThreadSafeQueue):
        QThread.__init__(self)
        self.queue = queue
        self.running = False

    @staticmethod
    def frequency_to_note(frequency):
        h = round(12 * np.log2(frequency / InstrumentTuner.C0))
        octave = h // 12
        n = h % 12
        return f"{InstrumentTuner.NOTE_NAMES[n]}{octave}"
    
    @staticmethod
    def note_to_frequency(note: str):
        if len(note) == 0:
            return -1
        
        if note[-1].isdigit():
            note_name = note[:-1]
            octave = int(note[-1])
        else:
            note_name = note
            octave = 4

        if note_name not in InstrumentTuner.NOTE_NAMES:
            return -1
        n = InstrumentTuner.NOTE_NAMES.index(note_name)
        return InstrumentTuner.C0 * 2 ** ((n + octave * 12) / 12)

    def run(self):
        self.running = True

        while self.running:
            frequency = self.queue.pop()
            if frequency is not None and frequency > 0:
                self.frequency_detected.emit(frequency)
            else:
                time.sleep(0.5)

    def stop(self):
        self.running = False
        self.queue.clear()
        self.queue.push(None)