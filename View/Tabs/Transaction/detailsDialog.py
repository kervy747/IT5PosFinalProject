from PyQt6.QtWidgets import *
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt
from View.components import *
from receipt_generator import ReceiptGenerator


class TransactionDetailsDialog(QDialog):
    """Dialog to show detailed transaction information with Print Receipt option"""

    def __init__(self, transaction, parent=None):
        super().__init__(parent)
        self.transaction = transaction
        self.receipt_generator = ReceiptGenerator(receipt_folder="receipts")
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
        items_table = StyledTable(5, ["ID", "Product Name", "Quantity", "Unit Price", "Total"])
        items_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        items_table.setRowCount(len(self.transaction.items))

        for i, item in enumerate(self.transaction.items):
            # ID
            id_item = QTableWidgetItem(str(item['product_id']))
            id_item.setFont(QFont("Poppins", 9, QFont.Weight.Medium))
            id_item.setForeground(QColor("#006D77"))
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

            # Unit Price
            price_item = QTableWidgetItem(f"₱{item['price']:,.2f}")
            price_item.setFont(QFont("Poppins", 9, QFont.Weight.Bold))
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            items_table.setItem(i, 3, price_item)

            # Item Total (price * quantity)
            item_total = item['price'] * item['quantity']
            total_item = QTableWidgetItem(f"₱{item_total:,.2f}")
            total_item.setFont(QFont("Poppins", 9, QFont.Weight.Bold))
            total_item.setForeground(QColor("#006D77"))
            total_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            items_table.setItem(i, 4, total_item)

        items_table.setColumnWidth(0, 80)
        items_table.setColumnWidth(2, 80)
        items_table.setColumnWidth(3, 110)
        items_table.setColumnWidth(4, 110)

        layout.addWidget(items_table)

        # Buttons row - Print Receipt + Close
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Print Receipt button
        print_btn = QPushButton("🖨  Print Receipt")
        print_btn.setMinimumHeight(45)
        print_btn.setMinimumWidth(180)
        print_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        print_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT};
                color: white;
                padding: 12px 30px;
                border-radius: 8px;
                font-family: Poppins;
                font-size: 11pt;
                font-weight: bold;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #6FAAA4;
            }}
            QPushButton:pressed {{
                background-color: #5A9489;
            }}
        """)
        print_btn.clicked.connect(self.on_print_receipt)
        btn_layout.addWidget(print_btn)

        # Close button
        close_btn = QPushButton("✓  Close")
        close_btn.setMinimumHeight(45)
        close_btn.setMinimumWidth(180)
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY};
                color: white;
                padding: 12px 30px;
                border-radius: 8px;
                font-family: Poppins;
                font-size: 11pt;
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
        btn_layout.addWidget(close_btn)

        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def on_print_receipt(self):
        """Generate and open receipt for this transaction"""
        try:
            # Build a mock cart items list from transaction items
            # so receipt_generator can format it properly
            cart_items = []
            for item in self.transaction.items:
                cart_items.append(TransactionReceiptItem(
                    product_id=item['product_id'],
                    product_name=item['product_name'],
                    price=item['price'],
                    quantity=item['quantity']
                ))

            total_amount = self.transaction.total_amount

            # Generate receipt (cash and change unknown from history, so show total only)
            success, result = self.receipt_generator.generate_receipt(
                order_id=self.transaction.order_id,
                staff_name=self.transaction.staff_name,
                cart_items=cart_items,
                total_amount=total_amount,
                cash_amount=total_amount,  # We don't store cash/change, so just show total
                change_amount=0.00,
                transaction_date=self.transaction.date
            )

            if success:
                filepath = result

                # Custom styled dialog
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Receipt Generated")
                msg.setText(
                    f"Receipt saved successfully!\n\n"
                    f"📄 File: {filepath}\n\n"
                    f"Do you want to open it now?"
                )
                msg.setStyleSheet(f"""
                    QMessageBox {{
                        background-color: #1a1a2e;
                        color: white;
                        border-radius: 10px;
                    }}
                    QMessageBox QLabel {{
                        color: white;
                        font-family: Poppins;
                        font-size: 10pt;
                        background-color: transparent;
                    }}
                    QPushButton {{
                        background-color: {PRIMARY};
                        color: white;
                        padding: 8px 20px;
                        border-radius: 6px;
                        font-family: Poppins;
                        font-size: 10pt;
                        font-weight: bold;
                        border: none;
                        min-width: 90px;
                    }}
                    QPushButton:hover {{
                        background-color: #005662;
                    }}
                    QPushButton:pressed {{
                        background-color: #004a54;
                    }}
                """)

                yes_btn = msg.addButton("Yes", QMessageBox.ButtonRole.AcceptRole)
                no_btn = msg.addButton("No", QMessageBox.ButtonRole.RejectRole)
                msg.exec()

                if msg.clickedButton() == yes_btn:
                    self.receipt_generator.open_receipt(filepath)
            else:
                QMessageBox.critical(
                    self,
                    "Receipt Error",
                    f"Failed to generate receipt:\n\n{result}"
                )

        except Exception as e:
            print(f"Error printing receipt: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(
                self,
                "Receipt Error",
                f"An error occurred while generating the receipt:\n\n{str(e)}"
            )


class TransactionReceiptItem:
    """
    Wrapper class to mimic CartItem structure
    so receipt_generator can format transaction items properly.
    """

    def __init__(self, product_id, product_name, price, quantity):
        self.product = TransactionReceiptProduct(product_id, product_name, price)
        self.quantity = quantity

    def get_total(self):
        return self.product.price * self.quantity


class TransactionReceiptProduct:
    """
    Wrapper class to mimic Product structure
    so receipt_generator can access product.name and product.price.
    """

    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = float(price)