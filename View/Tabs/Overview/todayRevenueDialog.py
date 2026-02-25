from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QFrame
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt
from datetime import datetime
from View.colors import *


class TodayRevenueDialog(QDialog):
    """Dialog showing all transactions for today"""

    def __init__(self, transactions, parent=None):
        super().__init__(parent)
        self.transactions = self._filter_today(transactions)
        self.setWindowTitle("Today's Revenue")
        self.setMinimumSize(750, 520)
        self.setStyleSheet(f"QDialog {{ background-color: {BACKGROUND}; }}")
        self.init_ui()

    def _filter_today(self, transactions):
        today = datetime.now().date()
        filtered = []
        for t in transactions:
            try:
                if hasattr(t, 'created_at') and t.created_at:
                    trans_date = t.created_at
                elif hasattr(t, 'date') and t.date:
                    trans_date = datetime.strptime(t.date, "%m-%d-%Y %I:%M %p")
                else:
                    continue
                if trans_date.date() == today:
                    filtered.append(t)
            except Exception:
                continue
        # Sort newest first
        filtered.sort(
            key=lambda t: t.created_at if hasattr(t, 'created_at') and t.created_at
            else datetime.strptime(t.date, "%m-%d-%Y %I:%M %p"),
            reverse=True
        )
        return filtered

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(18)

        # ── Header ──────────────────────────────────────────────────
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {PRIMARY};
                border-radius: 10px;
            }}
        """)
        header_inner = QVBoxLayout(header_frame)
        header_inner.setContentsMargins(20, 16, 20, 16)
        header_inner.setSpacing(4)

        title = QLabel("💰  Today's Revenue")
        title.setFont(QFont("Poppins", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: white; background: transparent;")
        header_inner.addWidget(title)

        today_str = datetime.now().strftime("%A, %B %d, %Y")
        subtitle = QLabel(today_str)
        subtitle.setFont(QFont("Poppins", 10))
        subtitle.setStyleSheet("color: rgba(255,255,255,0.85); background: transparent;")
        header_inner.addWidget(subtitle)

        layout.addWidget(header_frame)

        # ── Summary strip ────────────────────────────────────────────
        summary_row = QHBoxLayout()
        summary_row.setSpacing(12)

        total_revenue = sum(t.total_amount for t in self.transactions)
        tx_count = len(self.transactions)
        avg = total_revenue / tx_count if tx_count else 0

        for label, value in [
            ("Transactions", str(tx_count)),
            ("Total Revenue", f"₱{total_revenue:,.2f}"),
            ("Avg per Sale", f"₱{avg:,.2f}"),
        ]:
            card = self._mini_card(label, value)
            summary_row.addWidget(card)

        layout.addLayout(summary_row)

        # ── Table ────────────────────────────────────────────────────
        cols = ["Order ID", "Staff", "Time", "Items", "Total Amount"]
        self.table = QTableWidget(len(self.transactions), len(cols))
        self.table.setHorizontalHeaderLabels(cols)
        self.table.setFont(QFont("Poppins", 9))
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.horizontalHeader().setFont(QFont("Poppins", 9, QFont.Weight.Bold))
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {WHITE};
                border: none;
                border-radius: 10px;
                gridline-color: transparent;
            }}
            QTableWidget::item {{
                padding: 10px 12px;
                color: #2C3E50;
            }}
            QTableWidget::item:selected {{
                background-color: {PRIMARY}22;
                color: {PRIMARY};
            }}
            QHeaderView::section {{
                background-color: {PRIMARY};
                color: white;
                padding: 10px 12px;
                border: none;
                font-family: Poppins;
                font-size: 9pt;
                font-weight: bold;
            }}
            QTableWidget::item:alternate {{
                background-color: #F8FAFC;
            }}
        """)

        if self.transactions:
            for row, t in enumerate(self.transactions):
                try:
                    if hasattr(t, 'created_at') and t.created_at:
                        time_str = t.created_at.strftime("%I:%M %p")
                    else:
                        time_str = t.date.split(" ", 1)[1] if " " in t.date else t.date
                except Exception:
                    time_str = "—"

                total_items = t.get_total_items() if hasattr(t, 'get_total_items') else len(t.items)

                cells = [
                    (t.order_id, Qt.AlignmentFlag.AlignLeft, PRIMARY),
                    (t.staff_name, Qt.AlignmentFlag.AlignLeft, "#2C3E50"),
                    (time_str, Qt.AlignmentFlag.AlignCenter, "#64748B"),
                    (str(total_items), Qt.AlignmentFlag.AlignCenter, "#2C3E50"),
                    (f"₱{t.total_amount:,.2f}", Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, PRIMARY),
                ]

                for col, (text, align, color) in enumerate(cells):
                    item = QTableWidgetItem(text)
                    item.setFont(QFont("Poppins", 9,
                                       QFont.Weight.Bold if col in (0, 4) else QFont.Weight.Normal))
                    item.setTextAlignment(align)
                    item.setForeground(QColor(color))
                    self.table.setItem(row, col, item)

                self.table.setRowHeight(row, 44)
        else:
            self.table.setRowCount(1)
            empty = QTableWidgetItem("No transactions recorded today")
            empty.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setFont(QFont("Poppins", 10))
            empty.setForeground(QColor("#94A3B8"))
            self.table.setItem(0, 0, empty)
            self.table.setSpan(0, 0, 1, len(cols))

        layout.addWidget(self.table)

        # ── Close button ─────────────────────────────────────────────
        close_btn = QPushButton("✓  Close")
        close_btn.setFixedHeight(42)
        close_btn.setFixedWidth(140)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setFont(QFont("Poppins", 10, QFont.Weight.Bold))
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY};
                color: white;
                border-radius: 8px;
                border: none;
            }}
            QPushButton:hover {{ background-color: #005662; }}
            QPushButton:pressed {{ background-color: #004a54; }}
        """)
        close_btn.clicked.connect(self.close)

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(close_btn)
        layout.addLayout(btn_row)

    def _mini_card(self, label, value):
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {WHITE};
                border-radius: 10px;
                border: none;
            }}
        """)
        frame.setFixedHeight(68)
        inner = QVBoxLayout(frame)
        inner.setContentsMargins(16, 10, 16, 10)
        inner.setSpacing(2)

        lbl = QLabel(label)
        lbl.setFont(QFont("Poppins", 8, QFont.Weight.Medium))
        lbl.setStyleSheet("color: #64748B; background: transparent;")
        inner.addWidget(lbl)

        val = QLabel(value)
        val.setFont(QFont("Poppins", 14, QFont.Weight.Bold))
        val.setStyleSheet(f"color: {PRIMARY}; background: transparent;")
        inner.addWidget(val)

        return frame