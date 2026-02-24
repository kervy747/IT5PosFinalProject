from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QLinearGradient, QFont
from PyQt6.QtCore import Qt


class BarChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = []
        self.labels = []
        self.setMinimumHeight(180)

    def set_data(self, labels, values):
        self.labels = labels
        self.data = values
        self.update()

    def paintEvent(self, event):
        if not self.data:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()
        padding_left = 55
        padding_right = 20
        padding_top = 20
        padding_bottom = 40

        chart_w = w - padding_left - padding_right
        chart_h = h - padding_top - padding_bottom

        max_val = max(self.data) if self.data else 1
        if max_val == 0:
            max_val = 1

        grid_lines = 4
        for i in range(grid_lines + 1):
            y = padding_top + chart_h - (i / grid_lines) * chart_h
            painter.setPen(QPen(QColor("#E1E8ED"), 1))
            painter.drawLine(padding_left, int(y), padding_left + chart_w, int(y))
            val = (i / grid_lines) * max_val
            painter.setPen(QPen(QColor("#6c757d"), 1))
            painter.setFont(QFont("Poppins", 7))
            painter.drawText(0, int(y) - 6, padding_left - 5, 16,
                             Qt.AlignmentFlag.AlignRight, f"₱{val:,.0f}")

        n = len(self.data)
        bar_spacing = 6
        bar_w = max(8, (chart_w - (n + 1) * bar_spacing) // n)

        for i, (val, label) in enumerate(zip(self.data, self.labels)):
            bar_h = int((val / max_val) * chart_h) if max_val > 0 else 0
            x = padding_left + bar_spacing + i * (bar_w + bar_spacing)
            y = padding_top + chart_h - bar_h

            gradient = QLinearGradient(x, y, x, y + bar_h)
            gradient.setColorAt(0, QColor("#006D77"))
            gradient.setColorAt(1, QColor("#83C5BE"))
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(x, y, bar_w, bar_h, 4, 4)

            painter.setPen(QPen(QColor("#2c3e50"), 1))
            painter.setFont(QFont("Poppins", 7))
            painter.drawText(x - 5, padding_top + chart_h + 4, bar_w + 10, 16,
                             Qt.AlignmentFlag.AlignCenter, label)

            if val > 0:
                painter.setPen(QPen(QColor("#006D77"), 1))
                painter.setFont(QFont("Poppins", 6, QFont.Weight.Bold))
                painter.drawText(x - 5, y - 14, bar_w + 10, 14,
                                 Qt.AlignmentFlag.AlignCenter, f"₱{val:,.0f}")

        painter.end()