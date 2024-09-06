from styling.StyleManager import StyleManager

import numpy as np
from PyQt6.QtCore import QPointF, QRectF, Qt
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QColor, QFont, QPainter, QPen, QPolygonF

class Speedometer(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.frequency = 440.0
        self.target_frequency = 440.0
        self.maximum_needle_deviation = 40

        self.style_manager = StyleManager()

    def update_frequency(self, frequency, target_frequency):
        self.frequency = frequency
        self.target_frequency = target_frequency
        self.update()

    def draw_deviation_zones(self, painter: QPainter, center, radius):
        colors = self.style_manager.deviation_zone_colors
        for i in range(len(colors)):
            start_angle = 180 - i * self.style_manager.zone_span
            color = colors[i]

            painter.setPen(self.style_manager.black)
            painter.setBrush(color)
            painter.drawPie(
                int(center.x() - radius),
                int(center.y() - radius),
                int(2 * radius),
                int(2 * radius),
                int(start_angle * 16),
                int(-self.style_manager.zone_span * 16)
            )

    def draw_needle(self, painter: QPainter, center, radius):
        needle_length = radius * 0.95
        needle_width = 8

        needle_angle = self.calculate_needle_angle()

        painter.setPen(QPen(self.style_manager.black))
        painter.setBrush(self.style_manager.mid_gray)
        polygon = QPolygonF([
            QPointF(center.x(), center.y()),
            QPointF(center.x() + needle_length * np.cos(np.radians(needle_angle)),
                    center.y() - needle_length * np.sin(np.radians(needle_angle))),
            QPointF(center.x() + needle_width * np.cos(np.radians(needle_angle + 90)),
                    center.y() - needle_width * np.sin(np.radians(needle_angle + 90)))
        ])
        painter.drawPolygon(polygon)

        painter.setBrush(self.style_manager.light_gray)
        polygon = QPolygonF([
            QPointF(center.x(), center.y()),
            QPointF(center.x() + needle_length * np.cos(np.radians(needle_angle)),
                    center.y() - needle_length * np.sin(np.radians(needle_angle))),
            QPointF(center.x() + needle_width * np.cos(np.radians(needle_angle - 90)),
                    center.y() - needle_width * np.sin(np.radians(needle_angle - 90)))
        ])
        painter.drawPolygon(polygon)

    def draw_pivot(self, painter: QPainter, center):
        outer_radius = self.style_manager.pivot_outer_radius
        inner_radius = self.style_manager.pivot_inner_radius
        
        painter.setPen(QPen(self.style_manager.black))
        painter.setBrush(self.style_manager.light_gray)
        painter.drawEllipse(int(center.x() - outer_radius),
                            int(center.y() - outer_radius),
                            int(outer_radius * 2),
                            int(outer_radius * 2))
        
        painter.setBrush(QColor(128, 128, 128))
        painter.drawEllipse(int(center.x() - inner_radius),
                            int(center.y() - inner_radius),
                            int(inner_radius * 2),
                            int(inner_radius * 2))
        
    def draw_labels(self, painter: QPainter, center, radius):
        label_font = QFont(self.style_manager.font, 16)
        painter.setFont(label_font)
        painter.setPen(QPen(self.style_manager.white))
        labels = ['-40', '-30', '-20', '-10', '0', '+10', '+20', '+30', '+40']
        label_radius = radius + 20

        for i in range(len(labels)):
            angle_rad = np.radians(self.style_manager.speedometer_span - i * (self.style_manager.speedometer_span / (len(labels) - 1)))
            label_x = center.x() + np.cos(angle_rad) * label_radius
            label_y = center.y() - np.sin(angle_rad) * label_radius

            text_rect = painter.boundingRect(QRectF(), Qt.AlignmentFlag.AlignCenter, labels[i])
            label_x -= text_rect.width() / 2
            label_y += text_rect.height() / 2

            painter.drawText(QPointF(label_x, label_y), labels[i])

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        center = self.rect().center()
        center.setY(int(center.y() + self.height() * 0.35))

        radius = min(self.width(), self.height()) / 1.35 - min(self.width(), self.height()) / 9
        self.draw_deviation_zones(painter, center, radius)
        self.draw_needle(painter, center, radius)
        self.draw_pivot(painter, center)
        self.draw_labels(painter, center, radius)

    def calculate_needle_angle(self):
        deviation = max(
            -self.maximum_needle_deviation,
            min(self.frequency - self.target_frequency, self.maximum_needle_deviation)
        )
        return 90 - (deviation / self.maximum_needle_deviation) * 90