from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QFrame, QProgressBar
)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt
from datetime import datetime
from View.colors import *


class AvgTransactionDialog(QDialog):
    """
    Dialog showing average transaction breakdown for the selected month.

    Displays:
    • Key stats  — avg, median, lowest, highest
    • A simple amount-range distribution (bar-style)
    • Full sorted transaction table for the month
    """

    def __init__(self, transactions, month_name, year, parent=None):
        super().__init__(parent)
        self.transactions = transactions
        self.month_name = month_name
        self.year = year
        self.setWindowTitle(f"Avg. Transaction Breakdown — {month_name} {year}")
        self.setMinimumSize(780, 600)
        self.setStyleSheet(f"QDialog {{ background-color: {BACKGROUND}; }}")
        self._stats = self._compute_stats()
        self.init_ui()

    # ── Computation ──────────────────────────────────────────────────────────

    def _compute_stats(self):
        amounts = sorted(t.total_amount for t in self.transactions)
        n = len(amounts)
        if n == 0:
            return dict(count=0, total=0, avg=0, median=0,
                        min_val=0, max_val=0, buckets=[])

        total = sum(amounts)
        avg = total / n
        median = amounts[n // 2] if n % 2 != 0 else (amounts[n // 2 - 1] + amounts[n // 2]) / 2

        lo, hi = amounts[0], amounts[-1]
        buckets = []
        if lo == hi:
            buckets = [(f"₱{lo:,.0f}", n)]
        else:
            width = (hi - lo) / 5
            for i in range(5):
                b_lo = lo + i * width
                b_hi = lo + (i + 1) * width
                label = f"₱{b_lo:,.0f}–{b_hi:,.0f}"
                count = sum(1 for a in amounts if b_lo <= a <= b_hi)
                buckets.append((label, count))

        return dict(count=n, total=total, avg=avg, median=median,
                    min_val=amounts[0], max_val=amounts[-1], buckets=buckets)

    # ── UI ───────────────────────────────────────────────────────────────────

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(16)

        # ── Header ────────────────────────────────────────────────────
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{ background-color: {PRIMARY}; border-radius: 10px; }}
        """)
        h_inner = QVBoxLayout(header_frame)
        h_inner.setContentsMargins(20, 14, 20, 14)
        h_inner.setSpacing(4)

        title = QLabel(f"💳  Average Transaction — {self.month_name} {self.year}")
        title.setFont(QFont("Poppins", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: white; background: transparent;")
        h_inner.addWidget(title)

        sub = QLabel(
            f"{self._stats['count']} transaction{'s' if self._stats['count'] != 1 else ''} "
            f"· Total ₱{self._stats['total']:,.2f}"
        )
        sub.setFont(QFont("Poppins", 9))
        sub.setStyleSheet("color: rgba(255,255,255,0.85); background: transparent;")
        h_inner.addWidget(sub)

        layout.addWidget(header_frame)

        # ── Stat pills ────────────────────────────────────────────────
        cards_row = QHBoxLayout()
        cards_row.setSpacing(10)

        stat_defs = [
            ("Average",  f"₱{self._stats['avg']:,.2f}",     PRIMARY),
            ("Median",   f"₱{self._stats['median']:,.2f}",  ACCENT),
            ("Lowest",   f"₱{self._stats['min_val']:,.2f}", TEXT_DARK),
            ("Highest",  f"₱{self._stats['max_val']:,.2f}", TEXT_DARK),
        ]
        for label, value, color in stat_defs:
            cards_row.addWidget(self._mini_stat(label, value, color))

        layout.addLayout(cards_row)

        # ── Distribution bars ─────────────────────────────────────────
        if self._stats['count'] > 1:
            dist_frame = QFrame()
            dist_frame.setStyleSheet(f"""
                QFrame {{ background-color: {WHITE}; border-radius: 10px; }}
            """)
            dist_inner = QVBoxLayout(dist_frame)
            dist_inner.setContentsMargins(16, 12, 16, 14)
            dist_inner.setSpacing(8)

            dist_title = QLabel("Amount Distribution")
            dist_title.setFont(QFont("Poppins", 10, QFont.Weight.Bold))
            dist_title.setStyleSheet(f"color: {TEXT_DARK}; background: transparent;")
            dist_inner.addWidget(dist_title)

            max_count = max(c for _, c in self._stats['buckets']) or 1
            for range_label, count in self._stats['buckets']:
                row = QHBoxLayout()
                row.setSpacing(10)

                range_lbl = QLabel(range_label)
                range_lbl.setFixedWidth(160)
                range_lbl.setFont(QFont("Poppins", 8))
                range_lbl.setStyleSheet(f"color: {TEXT_DARK}; background: transparent;")
                row.addWidget(range_lbl)

                bar = QProgressBar()
                bar.setRange(0, max_count)
                bar.setValue(count)
                bar.setFixedHeight(18)
                bar.setTextVisible(False)
                bar.setStyleSheet(f"""
                    QProgressBar {{
                        background-color: {BACKGROUND};
                        border-radius: 9px;
                        border: none;
                    }}
                    QProgressBar::chunk {{
                        background-color: {PRIMARY};
                        border-radius: 9px;
                    }}
                """)
                row.addWidget(bar, 1)

                count_lbl = QLabel(str(count))
                count_lbl.setFixedWidth(28)
                count_lbl.setFont(QFont("Poppins", 8, QFont.Weight.Bold))
                count_lbl.setStyleSheet(f"color: {PRIMARY}; background: transparent;")
                count_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                row.addWidget(count_lbl)

                dist_inner.addLayout(row)

            layout.addWidget(dist_frame)

        # ── Table ─────────────────────────────────────────────────────
        table_label = QLabel("All Transactions (sorted by amount)")
        table_label.setFont(QFont("Poppins", 10, QFont.Weight.Bold))
        table_label.setStyleSheet(f"color: {TEXT_DARK};")
        layout.addWidget(table_label)

        sorted_txns = sorted(self.transactions, key=lambda t: t.total_amount, reverse=True)

        cols = ["Order ID", "Staff", "Date", "Items", "Total Amount"]
        self.table = QTableWidget(len(sorted_txns), len(cols))
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
            }}
            QTableWidget::item {{
                padding: 8px 12px;
                color: {TEXT_DARK};
            }}
            QTableWidget::item:selected {{
                background-color: {ACCENT}40;
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
            QTableWidget::item:alternate {{ background-color: {BACKGROUND}; }}
        """)

        for row, t in enumerate(sorted_txns):
            try:
                if hasattr(t, 'created_at') and t.created_at:
                    date_str = t.created_at.strftime("%b %d, %I:%M %p")
                else:
                    date_str = t.date
            except Exception:
                date_str = "—"

            total_items = t.get_total_items() if hasattr(t, 'get_total_items') else len(t.items)

            cells = [
                (t.order_id,               Qt.AlignmentFlag.AlignLeft,                                   PRIMARY),
                (t.staff_name,             Qt.AlignmentFlag.AlignLeft,                                   TEXT_DARK),
                (date_str,                 Qt.AlignmentFlag.AlignCenter,                                 TEXT_DARK),
                (str(total_items),         Qt.AlignmentFlag.AlignCenter,                                 TEXT_DARK),
                (f"₱{t.total_amount:,.2f}", Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter, PRIMARY),
            ]

            for col, (text, align, color) in enumerate(cells):
                item = QTableWidgetItem(text)
                item.setFont(QFont("Poppins", 9,
                                   QFont.Weight.Bold if col in (0, 4) else QFont.Weight.Normal))
                item.setTextAlignment(align)
                item.setForeground(QColor(color))
                self.table.setItem(row, col, item)

            self.table.setRowHeight(row, 40)

        if not sorted_txns:
            self.table.setRowCount(1)
            empty = QTableWidgetItem("No transactions for this month")
            empty.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setFont(QFont("Poppins", 10))
            empty.setForeground(QColor(ACCENT))
            self.table.setItem(0, 0, empty)
            self.table.setSpan(0, 0, 1, len(cols))

        layout.addWidget(self.table)

        # ── Close button ──────────────────────────────────────────────
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

    def _mini_stat(self, label, value, color):
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
        inner.setContentsMargins(14, 10, 14, 10)
        inner.setSpacing(2)

        lbl = QLabel(label)
        lbl.setFont(QFont("Poppins", 8, QFont.Weight.Medium))
        lbl.setStyleSheet(f"color: #64748B; background: transparent;")
        inner.addWidget(lbl)

        val = QLabel(value)
        val.setFont(QFont("Poppins", 13, QFont.Weight.Bold))
        val.setStyleSheet(f"color: {color}; background: transparent;")
        inner.addWidget(val)

        return frame