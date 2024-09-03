import numpy as np

from PyQt6.QtCore import QPoint, QRectF, Qt, QPointF, QSize
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QColor, QFont, QPainter, QPen

class Speedometer(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.frequency = 440.0
        self.target_frequency = 440.0
        self.maximum_needle_deviation = 40

        self.setFixedSize(400, 280)

    def update_frequency(self, frequency, target_frequency):
        self.frequency = frequency
        self.target_frequency = target_frequency
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        center = self.rect().center()
        center.setY(center.y() + 100)

        radius = min(self.width(), self.height()) / 1.375 - min(self.width(), self.height()) / 8

        needle_zones = 8
        total_angle_span = 180
        angle_increment = total_angle_span / needle_zones

        colors = [
            QColor(255, 0, 0),
            QColor(255, 128, 0),
            QColor(255, 191, 0),
            QColor(0, 255, 0),
            QColor(0, 255, 0),
            QColor(255, 191, 0),
            QColor(255, 128, 0),
            QColor(255, 0, 0)
        ]

        for i in range(needle_zones):
            start_angle = total_angle_span - i * angle_increment

            color = colors[i]

            painter.setPen(QPen(QColor(0, 0, 0)))
            painter.setBrush(color)
            painter.drawPie(
                int(center.x() - radius),
                int(center.y() - radius),
                int(2 * radius),
                int(2 * radius),
                int(start_angle * 16),
                int(-angle_increment * 16)
            )

        needle_angle = self.calculate_needle_angle()

        painter.setPen(QPen(QColor(0, 0, 0), 5))
        painter.drawLine(
            center,
            center + QPoint(radius * np.cos(np.radians(needle_angle)), -radius * np.sin(np.radians(needle_angle)))
        )

        label_font = QFont('Digital-7', 16)
        painter.setFont(label_font)
        painter.setPen(QPen(QColor(255, 255, 255)))
        labels = ['-40', '-30', '-20', '-10', '0', '+10', '+20', '+30', '+40']
        label_radius = radius + 20

        for i in range(len(labels)):
            angle_rad = np.radians(180 - i * (total_angle_span / (len(labels) - 1)))
            label_x = center.x() + np.cos(angle_rad) * label_radius
            label_y = center.y() - np.sin(angle_rad) * label_radius

            text_rect = painter.boundingRect(QRectF(), Qt.AlignmentFlag.AlignCenter, labels[i])
            label_x -= text_rect.width() / 2
            label_y += text_rect.height() / 2

            painter.drawText(QPointF(label_x, label_y), labels[i])

    def calculate_needle_angle(self):
        max_deviation = 40.0
        deviation = max(-max_deviation, min(self.frequency - self.target_frequency, max_deviation))
        
        return 90 - (deviation / max_deviation) * 90
