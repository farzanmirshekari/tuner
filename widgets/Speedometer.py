from PyQt6.QtWidgets import QWidget

class Speedometer(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.frequency = 440.0
        self.target_frequency = 440.0
        self.setMinimumSize(400, 500)

    def update_frequency(self, frequency, target_frequency):
        self.frequency = frequency
        self.target_frequency = target_frequency
        self.update()

    def paintEvent(self, event):
        pass

    def calculate_needle_angle(self):
        pass