from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from View.colors import *


class TopProductCard(QFrame):

    def __init__(self, rank, name, quantity, revenue):
        super().__init__()
        self.rank = rank
        self.name = name
        self.quantity = quantity
        self.revenue = revenue
        self.init_ui()

    def init_ui(self):
        rank_colors = {
            1: ("#FFD700", "#FFA500"),  # Gold
            2: ("#C0C0C0", "#A8A8A8"),  # Silver
            3: ("#CD7F32", "#B8860B"),  # Bronze
            4: (PRIMARY, ACCENT),
            5: (ACCENT, "#6BA8A0")
        }

        bg_color, accent_color = rank_colors.get(self.rank, (PRIMARY, ACCENT))

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {WHITE};
                border-radius: 12px;
                border: 1px solid {WHITE};
            }}
            QFrame:hover {{
                background-color: {BACKGROUND};
                border: 1px solid {ACCENT};
            }}
        """)
        self.setMinimumHeight(70)

        layout = QHBoxLayout()
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(14)

        # Rank badge
        rank_container = QFrame()
        rank_container.setFixedSize(45, 45)
        rank_container.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {bg_color}, stop:1 {accent_color});
                border-radius: 22px;
                border: 3px solid {WHITE};
            }}
        """)

        rank_layout = QVBoxLayout(rank_container)
        rank_layout.setContentsMargins(0, 0, 0, 0)

        rank_label = QLabel(str(self.rank))
        rank_label.setFont(QFont("Poppins", 16, QFont.Weight.Bold))
        rank_label.setStyleSheet(f"color: {WHITE}; border: none; background: transparent;")
        rank_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rank_layout.addWidget(rank_label)

        layout.addWidget(rank_container)

        # Product name
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)

        name_label = QLabel(self.name)
        name_label.setFont(QFont("Poppins", 12, QFont.Weight.DemiBold))
        name_label.setStyleSheet(f"color: {TEXT_DARK}; background: transparent;")
        info_layout.addWidget(name_label)

        layout.addLayout(info_layout)
        layout.addStretch()

        units_layout = QVBoxLayout()
        units_layout.setSpacing(2)
        units_layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        units_value = QLabel(str(self.quantity))
        units_value.setFont(QFont("Poppins", 18, QFont.Weight.Bold))
        units_value.setStyleSheet(f"color: {bg_color}; background: transparent;")
        units_value.setAlignment(Qt.AlignmentFlag.AlignRight)

        units_text = QLabel("units sold")
        units_text.setFont(QFont("Poppins", 9))
        units_text.setStyleSheet("color: #64748B; background: transparent;")
        units_text.setAlignment(Qt.AlignmentFlag.AlignRight)

        units_layout.addWidget(units_value)
        units_layout.addWidget(units_text)

        layout.addLayout(units_layout)

        self.setLayout(layout)