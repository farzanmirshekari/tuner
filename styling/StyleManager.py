from PyQt6.QtGui import QColor

class StyleManager:

    def __init__(self):
        self.red_deviation_zone = QColor(255, 0, 0)
        self.orange_deviation_zone = QColor(255, 128, 0)
        self.yellow_deviation_zone = QColor(255, 191, 0)
        self.green_deviation_zone = QColor(0, 255, 0)
        
        self.black = QColor(0, 0, 0)
        self.white = QColor(255, 255, 255)
        self.light_gray = QColor(192, 192, 192)
        self.mid_gray = QColor(128, 128, 128)

        self.font = "Digital-7"
        
        self.deviation_zones = 8
        self.speedometer_span  = 180
        self.zone_span = self.speedometer_span / self.deviation_zones
        self.deviation_zone_colors = [
            self.red_deviation_zone,
            self.orange_deviation_zone,
            self.yellow_deviation_zone,
            self.green_deviation_zone,
            self.green_deviation_zone,
            self.yellow_deviation_zone,
            self.orange_deviation_zone,
            self.red_deviation_zone
        ]

        self.pivot_outer_radius = 8 
        self.pivot_inner_radius = self.pivot_outer_radius / 2