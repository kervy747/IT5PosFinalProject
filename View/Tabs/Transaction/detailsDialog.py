from PyQt6.QtWidgets import *
from View.components import *

class TransactionDetailsDialog(QDialog):
    """Dialog to show detailed transaction information"""

    def __init__(self, transaction, parent=None):
        super().__init__(parent)
        self.transaction = transaction
        self.setWindowTitle(f"Transaction Details - {transaction.order_id}")
        self.setMinimumSize(800, 600)
        self.setStyleSheet(f"QDialog {{ background-color: {BACKGROUND}; }}")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header
        header_container = QWidget()
        header_container.setStyleSheet(f"""
            QWidget {{
                background-color: {PRIMARY};
                border-radius: 10px;
                padding: 20px;
            }}
        """)
        header_layout = QVBoxLayout(header_container)

        header = QLabel(f"Order ID: {self.transaction.order_id}")
        header.setFont(QFont("Poppins", 20, QFont.Weight.Bold))
        header.setStyleSheet("color: white;")
        header_layout.addWidget(header)

        subheader = QLabel("Transaction Details")
        subheader.setFont(QFont("Poppins", 11))
        subheader.setStyleSheet("color: rgba(255, 255, 255, 0.9);")
        header_layout.addWidget(subheader)

        layout.addWidget(header_container)

        # Info card
        info_card = CardFrame()
        info_layout = QGridLayout(info_card)
        info_layout.setContentsMargins(20, 20, 20, 20)
        info_layout.setSpacing(15)

        # Info labels
        labels = [
            ("Staff Name:", self.transaction.staff_name, 0, 0),
            ("Date:", self.transaction.date, 0, 2),
            ("Total Items:", str(self.transaction.get_total_items()), 1, 0),
            ("Total Amount:", f"₱{self.transaction.total_amount:,.2f}", 1, 2)
        ]

        for label_text, value_text, row, col in labels:
            label = FieldLabel(label_text)
            info_layout.addWidget(label, row, col)

            value = QLabel(value_text)
            value.setFont(QFont("Poppins", 10 if "Amount" not in label_text else 12,
                                QFont.Weight.Bold if "Amount" in label_text else QFont.Weight.Normal))
            value.setStyleSheet(f"color: {PRIMARY if 'Amount' in label_text else '#2c3e50'};")
            info_layout.addWidget(value, row, col + 1)

        layout.addWidget(info_card)

        # Items section
        items_title = SectionLabel("Items Sold", 14)
        items_title.setStyleSheet(f"color: {PRIMARY}; margin-top: 10px;")
        layout.addWidget(items_title)

        # Items table
        items_table = StyledTable(4, ["ID", "Product Name", "Quantity", "Price"])
        items_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        items_table.setRowCount(len(self.transaction.items))

        for i, item in enumerate(self.transaction.items):
            # ID
            id_item = QTableWidgetItem(str(item['product_id']))
            id_item.setFont(QFont("Poppins", 9, QFont.Weight.Medium))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            items_table.setItem(i, 0, id_item)

            # Name
            name_item = QTableWidgetItem(item['product_name'])
            name_item.setFont(QFont("Poppins", 9))
            items_table.setItem(i, 1, name_item)

            # Quantity
            qty_item = QTableWidgetItem(str(item['quantity']))
            qty_item.setFont(QFont("Poppins", 9))
            qty_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            items_table.setItem(i, 2, qty_item)

            # Price
            price_item = QTableWidgetItem(f"₱{item['price']:,.2f}")
            price_item.setFont(QFont("Poppins", 9, QFont.Weight.Bold))
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            items_table.setItem(i, 3, price_item)

        items_table.setColumnWidth(0, 60)
        items_table.setColumnWidth(2, 100)
        items_table.setColumnWidth(3, 120)

        layout.addWidget(items_table)

        # Close button
        close_btn = PrimaryButton("Close", "✓")
        close_btn.setMinimumHeight(45)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY};
                color: white;
                padding: 14px 30px;
                border-radius: 8px;
                font-family: Poppins;
                font-size: 12pt;
                font-weight: bold;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #005662;
            }}
            QPushButton:pressed {{
                background-color: #004a54;
            }}
        """)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)