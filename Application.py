from AudioStream import AudioStream
from InstrumentTuner import InstrumentTuner
from ThreadSafeQueue import ThreadSafeQueue

from styling.StyleManager import StyleManager
from widgets.Speedometer import Speedometer

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QVBoxLayout, QWidget

import sys

class MainWindow(QMainWindow):

    def __init__(self, queue: ThreadSafeQueue):
        super().__init__()
        self.queue = queue
        self.tuner_thread = InstrumentTuner(queue)

        self.target_frequency = InstrumentTuner.A4

        self.style_manager = StyleManager()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Instrument Tuner")

        self.setStyleSheet(self.style_manager.main_window_stylesheet)

        self.speedometer = Speedometer(self)
        self.speedometer.setFixedSize(self.style_manager.main_window_width, self.style_manager.main_window_height)

        self.note_input = QLineEdit(self)
        self.note_input.setPlaceholderText("Enter note (e.g., A4)")
        self.target_label = QLabel(f"Target Frequency: {InstrumentTuner.A4:.2f} Hz", self)
        self.freq_label = QLabel("Frequency: 0 Hz", self)

        label_layout = QVBoxLayout()
        label_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        label_layout.addWidget(self.note_input)
        label_layout.addWidget(self.target_label)
        label_layout.addWidget(self.freq_label)

        speedometer_layout = QHBoxLayout()
        speedometer_layout.addStretch()
        speedometer_layout.addWidget(self.speedometer)
        speedometer_layout.addStretch()

        layout = QVBoxLayout()
        layout.addLayout(label_layout)
        layout.addLayout(speedometer_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.note_input.textChanged.connect(self.update_note)

        self.tuner_thread.frequency_detected.connect(self.update_display)

        self.start_tuning()

    def start_tuning(self):
        self.tuner_thread.start()

    def stop_tuning(self):
        self.tuner_thread.stop()
        self.tuner_thread.wait()

    def update_display(self, frequency):
        self.freq_label.setText(f"Frequency: {frequency:.2f} Hz")
        self.speedometer.update_frequency(frequency, self.target_frequency)

    def update_note(self):
        note = self.note_input.text()
        frequency = InstrumentTuner.note_to_frequency(note)
        if frequency > 0:
            self.target_frequency = frequency
            self.target_label.setText(f"Target Frequency: {self.target_frequency:.2f} Hz")
        else:
            self.target_label.setText("Invalid note")

    def closeEvent(self, event: QCloseEvent):
        self.stop_tuning()
        event.accept()

if __name__ == "__main__":
    queue = ThreadSafeQueue()
    audio_stream = AudioStream(queue)
    audio_stream.start()

    app = QApplication(sys.argv)
    window = MainWindow(queue)
    window.show()

    def cleanup():
        audio_stream.stop()
        audio_stream.join()

        window.tuner_thread.stop()

    app.aboutToQuit.connect(cleanup)

    sys.exit(app.exec())