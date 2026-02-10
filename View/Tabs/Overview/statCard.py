from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from View.colors import *

class StatCard(QFrame):

    def __init__(self, title, value, icon="", trend=None, color=PRIMARY):
        super().__init__()
        self.title = title
        self.value_text = value
        self.icon = icon
        self.trend = trend
        self.color = color
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {WHITE};
                border-radius: 16px;
                border: none;
            }}  
        """)
        self.setMinimumHeight(140)
        self.setMaximumHeight(160)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(12)

        # Header with icon and title
        header_layout = QHBoxLayout()
        header_layout.setSpacing(0)

        # Icon circle
        if self.icon:
            icon_container = QFrame()
            icon_container.setFixedSize(48, 48)
            icon_container.setStyleSheet(f"""
                QFrame {{
                    background-color: transparent;  # ← Change this
                    border-radius: 24px;
                }}
            """)
            icon_layout = QVBoxLayout(icon_container)
            icon_layout.setContentsMargins(0, 0, 0, 0)

            icon_label = QLabel(self.icon)
            icon_label.setFont(QFont("Segoe UI Emoji", 20))
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_layout.addWidget(icon_label)

            header_layout.addWidget(icon_container)

        header_layout.addStretch()

        # Trend indicator
        if self.trend:
            trend_label = QLabel(self.trend)
            trend_label.setFont(QFont("Poppins", 10, QFont.Weight.Medium))
            trend_color = "#10B981" if "↑" in self.trend else "#EF4444" if "↓" in self.trend else "#6B7280"
            trend_label.setStyleSheet(f"""
                color: {trend_color};
                background-color: {trend_color}15;
                padding: 4px 10px;
                border-radius: 12px;
            """)
            header_layout.addWidget(trend_label)

        main_layout.addLayout(header_layout)

        # Title
        title_label = QLabel(self.title)
        title_label.setFont(QFont("Poppins", 11, QFont.Weight.Medium))
        title_label.setStyleSheet(f"color: #64748B;")
        main_layout.addWidget(title_label)

        # Value
        self.value_label = QLabel(self.value_text)
        self.value_label.setFont(QFont("Poppins", 26, QFont.Weight.Bold))
        self.value_label.setStyleSheet(f"color: {TEXT_DARK};")
        main_layout.addWidget(self.value_label)

        main_layout.addStretch()
        self.setLayout(main_layout)

    def update_value(self, value, trend=None):
        self.value_label.setText(value)
        if trend:
            self.trend = trend