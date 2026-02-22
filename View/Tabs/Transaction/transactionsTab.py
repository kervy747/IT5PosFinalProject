import os
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap, QIcon, QAction
from View.components import *
from .detailsDialog import TransactionDetailsDialog


class TransactionsTab(QWidget):
    search_transactions_signal = pyqtSignal(str)
    filter_by_month_signal = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        main_card = CardFrame()
        card_layout = QVBoxLayout(main_card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(15)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)

        logo_label = QLabel()
        icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "Assets", "transactionLogo.svg")
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        header_layout.addWidget(logo_label)

        header_layout.addWidget(SectionLabel("Transaction History", 18))
        header_layout.addStretch()

        self.month_selector = MonthYearSelector(start_year=2020)
        self.month_selector.setMaximumWidth(320)
        self.month_selector.month_changed.connect(
            lambda month, year: self.filter_by_month_signal.emit(month, year)
        )
        header_layout.addWidget(self.month_selector)

        card_layout.addLayout(header_layout)

        self.search_input = SearchInput("Search by Order ID or Staff Name...")

        search_icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "Assets", "searchIcon.svg")
        search_icon = QIcon(search_icon_path)
        search_action = QAction(search_icon, "", self.search_input)
        self.search_input.addAction(search_action, QLineEdit.ActionPosition.LeadingPosition)

        self.search_input.textChanged.connect(
            lambda: self.search_transactions_signal.emit(self.search_input.text()))

        card_layout.addWidget(self.search_input)

        self.transactions_table = StyledTable(7,
                                              ["Order ID", "Staff Name", "Items", "Item IDs", "Amount", "Date",
                                               "Actions"])
        self.transactions_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        card_layout.addWidget(self.transactions_table)

        layout.addWidget(main_card)

    def show_error(self, title, message):
        QMessageBox.warning(self, title, message)

    def show_info(self, title, message):
        QMessageBox.information(self, title, message)

    def show_question(self, title, message):
        reply = QMessageBox.question(
            self,
            title,
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes

    def show_transaction_details(self, transaction):
        dialog = TransactionDetailsDialog(transaction, self)
        dialog.exec()

    def update_transactions_table(self, transactions):
        self.transactions_table.setRowCount(len(transactions))
        for i, transaction in enumerate(transactions):
            order_item = QTableWidgetItem(transaction.order_id)
            order_item.setFont(QFont("Poppins", 10, QFont.Weight.Medium))
            self.transactions_table.setItem(i, 0, order_item)

            staff_item = QTableWidgetItem(transaction.staff_name)
            staff_item.setFont(QFont("Poppins", 10))
            self.transactions_table.setItem(i, 1, staff_item)

            items_count = QTableWidgetItem(str(transaction.get_total_items()))
            items_count.setFont(QFont("Poppins", 10))
            items_count.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.transactions_table.setItem(i, 2, items_count)

            item_ids = ", ".join(map(str, transaction.get_item_ids()))
            ids_item = QTableWidgetItem(item_ids)
            ids_item.setFont(QFont("Poppins", 9))
            self.transactions_table.setItem(i, 3, ids_item)

            amount_item = QTableWidgetItem(f"₱{transaction.total_amount:,.2f}")
            amount_item.setFont(QFont("Poppins", 10, QFont.Weight.Bold))
            amount_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.transactions_table.setItem(i, 4, amount_item)

            date_item = QTableWidgetItem(transaction.date)
            date_item.setFont(QFont("Poppins", 9))
            self.transactions_table.setItem(i, 5, date_item)

            view_btn = ViewButton("View Details")
            view_btn.setMinimumHeight(45)
            view_btn.setMinimumWidth(130)
            view_btn.clicked.connect(lambda checked, t=transaction: self.show_transaction_details(t))

            btn_container = QWidget()
            btn_layout = QHBoxLayout(btn_container)
            btn_layout.addWidget(view_btn)
            btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            btn_layout.setContentsMargins(10, 10, 10, 10)
            self.transactions_table.setCellWidget(i, 6, btn_container)

        self.transactions_table.setColumnWidth(0, 120)
        self.transactions_table.setColumnWidth(2, 80)
        self.transactions_table.setColumnWidth(3, 150)
        self.transactions_table.setColumnWidth(4, 120)
        self.transactions_table.setColumnWidth(5, 150)
        self.transactions_table.setColumnWidth(6, 180)

        for row in range(self.transactions_table.rowCount()):
            self.transactions_table.setRowHeight(row, 70)