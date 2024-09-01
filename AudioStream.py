from ThreadSafeQueue import ThreadSafeQueue

import numpy as np
from pyaudio import PyAudio, paInt16

import copy
from threading import Thread

class AudioStream(Thread):

    SAMPLING_RATE = 44100
    CHUNK_SIZE = 1024
    CHUNK_COUNT = 50
    ZERO_PADDING = 3
    
    def __init__(self, queue: ThreadSafeQueue):
        Thread.__init__(self)

        self.running = False

        self.queue = queue
        self.buffer = np.zeros(self.CHUNK_SIZE * self.CHUNK_COUNT, dtype=np.int16)
        self.hanning_window = np.hanning(len(self.buffer))

        try:
            self.audio_object = PyAudio()
            self.stream = self.audio_object.open(format=paInt16,
                                                 channels=1,
                                                 rate=self.SAMPLING_RATE,
                                                 input=True,
                                                 output=False,
                                                 frames_per_buffer=self.CHUNK_SIZE)
        except Exception as e:
            print(e)
            return
        
    @staticmethod
    def harmonic_product_spectrum(magnitude_data):
        hps_copy = copy.deepcopy(magnitude_data)
        for i in range(2, 4):
            magnitude_data[:-(-len(magnitude_data) // i)] *= hps_copy[::i]
        return magnitude_data
        
    def run(self):
        self.running = True

        while self.running:
            try:
                data = np.frombuffer(self.stream.read(self.CHUNK_SIZE, exception_on_overflow=False), dtype=np.int16)
                self.buffer = np.concatenate((self.buffer[self.CHUNK_SIZE:], data))

                windowed_data = self.buffer * self.hanning_window
                padded_data = np.pad(windowed_data, (0, len(self.hanning_window) * self.ZERO_PADDING), mode='constant')

                magnitude_data = abs(np.fft.fft(padded_data))
                magnitude_data = np.array_split(magnitude_data, 2)[0]

                magnitude_data = self.harmonic_product_spectrum(magnitude_data)

                frequencies = np.fft.fftfreq(int((len(magnitude_data) * 2) / 1), 1. / self.SAMPLING_RATE)

                self.queue.push(round(frequencies[np.argmax(magnitude_data)], 2))

            except Exception as e:
                print(e)
                break
        
        self.stop()

    def stop(self):
        self.running = False

        self.stream.stop_stream()
        self.stream.close()
        self.audio_object.terminate()