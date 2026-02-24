from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QLinearGradient, QFont
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPolygon


class LineChartWidget(QWidget):
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
        if not self.data or len(self.data) < 2:
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
        step = chart_w / (n - 1)

        points = []
        for i, val in enumerate(self.data):
            x = int(padding_left + i * step)
            y = int(padding_top + chart_h - (val / max_val) * chart_h)
            points.append(QPoint(x, y))

        gradient = QLinearGradient(0, padding_top, 0, padding_top + chart_h)
        gradient.setColorAt(0, QColor(0, 109, 119, 80))
        gradient.setColorAt(1, QColor(0, 109, 119, 0))
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        fill_points = [QPoint(padding_left, padding_top + chart_h)] + points + [QPoint(padding_left + chart_w, padding_top + chart_h)]
        painter.drawPolygon(QPolygon(fill_points))

        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setPen(QPen(QColor("#006D77"), 2))
        for i in range(len(points) - 1):
            painter.drawLine(points[i], points[i + 1])

        painter.setBrush(QBrush(QColor("#006D77")))
        painter.setPen(QPen(QColor("white"), 2))
        for pt in points:
            painter.drawEllipse(pt.x() - 4, pt.y() - 4, 8, 8)

        painter.setPen(QPen(QColor("#2c3e50"), 1))
        painter.setFont(QFont("Poppins", 7))
        for pt, label in zip(points, self.labels):
            painter.drawText(pt.x() - 20, padding_top + chart_h + 4, 40, 16,
                             Qt.AlignmentFlag.AlignCenter, label)

        painter.end()