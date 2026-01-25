from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt6.QtGui import QFont
from View.colors import PRIMARY


class MetricCard(QFrame):
    """Modern metric card with clean design"""

    def __init__(self, title, value, subtitle="", color=PRIMARY):
        super().__init__()
        self.title = title
        self.value_text = value
        self.subtitle = subtitle
        self.color = color
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 12px;
                border-left: 5px solid {self.color};
                border: 1px solid #E8F4F5;
            }}
            QFrame:hover {{
                border-left: 5px solid {self.color};
                box-shadow: 0 2px 8px rgba(0, 109, 119, 0.1);
            }}
        """)
        self.setMinimumHeight(120)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(10)

        # Title
        title_label = QLabel(self.title)
        title_label.setFont(QFont("Poppins", 11, QFont.Weight.Medium))
        title_label.setStyleSheet("color: #6c757d;")
        layout.addWidget(title_label)

        # Value
        self.value_label = QLabel(self.value_text)
        self.value_label.setFont(QFont("Poppins", 28, QFont.Weight.Bold))
        self.value_label.setStyleSheet(f"color: {self.color};")
        layout.addWidget(self.value_label)

        # Subtitle
        if self.subtitle:
            self.subtitle_label = QLabel(self.subtitle)
            self.subtitle_label.setFont(QFont("Poppins", 9))
            self.subtitle_label.setStyleSheet("color: #999999;")
            layout.addWidget(self.subtitle_label)

        self.setLayout(layout)

    def update_value(self, value, subtitle=""):
        """Update the card's value and optional subtitle"""
        self.value_label.setText(value)
        if subtitle and hasattr(self, 'subtitle_label'):
            self.subtitle_label.setText(subtitle)