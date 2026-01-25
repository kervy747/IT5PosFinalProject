from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class ProductRankItem(QFrame):
    """Custom widget for product ranking display"""

    def __init__(self, rank, name, quantity, color):
        super().__init__()
        self.rank = rank
        self.name = name
        self.quantity = quantity
        self.color = color
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 10px;
                border-left: 4px solid {self.color};
                border: 1px solid #f0f0f0;
            }}
            QFrame:hover {{
                background-color: #F8FAFB;
                border-left: 4px solid {self.color};
            }}
        """)
        self.setMinimumHeight(60)

        layout = QHBoxLayout()
        layout.setContentsMargins(15, 12, 15, 12)

        # Rank badge
        rank_label = QLabel(f"#{self.rank}")
        rank_label.setFont(QFont("Poppins", 20, QFont.Weight.Bold))
        rank_label.setStyleSheet(f"color: {self.color}; background: transparent;")
        rank_label.setFixedWidth(60)
        rank_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(rank_label)

        # Product name
        name_label = QLabel(self.name)
        name_label.setFont(QFont("Poppins", 12, QFont.Weight.Medium))
        name_label.setStyleSheet("color: #2c3e50; background: transparent;")
        layout.addWidget(name_label)

        layout.addStretch()

        # Quantity
        qty_label = QLabel(f"{self.quantity} sold")
        qty_label.setFont(QFont("Poppins", 12, QFont.Weight.Bold))
        qty_label.setStyleSheet(f"color: {self.color}; background: transparent;")
        layout.addWidget(qty_label)

        self.setLayout(layout)