from PyQt6.QtWidgets import *
from PyQt6.QtGui import QColor, QDoubleValidator
from View.components import *

class cartView(QWidget):
    remove_from_cart_signal = pyqtSignal(int)
    complete_sale_signal = pyqtSignal()  # ✅ Just emit signal, no validation

    def __init__(self):
        super().__init__()
        self.current_total = 0.0
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Cart header
        layout.addWidget(SectionLabel("Shopping Cart", 18))

        # Cart table - larger to see items
        self.cart_table = StyledTable(4, ["Product", "Price", "Qty", "Total"])
        self.cart_table.setMinimumHeight(250)
        layout.addWidget(self.cart_table)

        # Total section - smaller
        total_frame = TotalCard()
        total_layout = QVBoxLayout(total_frame)
        total_layout.setContentsMargins(10, 8, 10, 8)

        self.total_label = QLabel("Total: ₱0.00")
        self.total_label.setFont(QFont("Poppins", 16, QFont.Weight.Bold))
        self.total_label.setStyleSheet("color: white;")
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        total_layout.addWidget(self.total_label)

        layout.addWidget(total_frame)

        # Cash input section
        cash_frame = CardFrame()
        cash_layout = QVBoxLayout(cash_frame)
        cash_layout.setContentsMargins(15, 12, 15, 12)
        cash_layout.setSpacing(8)

        cash_layout.addWidget(FieldLabel("Cash Amount"))

        self.cash_input = QLineEdit()
        self.cash_input.setPlaceholderText("Enter cash amount")
        validator = QDoubleValidator(0.0, 999999.99, 2)
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.cash_input.setValidator(validator)
        self.cash_input.textChanged.connect(self.calculate_change)
        self.cash_input.setStyleSheet("""
            QLineEdit {
                color: black;
                font-family: Poppins;
                font-size: 14px;
                background-color: #F8FAFB;
                padding: 10px;
                border: 2px solid #E1E8ED;
                border-radius: 8px;
            }
            QLineEdit:focus {
                border: 2px solid #006D77;
                background-color: white;
            }
        """)
        cash_layout.addWidget(self.cash_input)

        # Change label
        self.change_label = QLabel("Change: ₱0.00")
        self.change_label.setFont(QFont("Poppins", 14, QFont.Weight.Bold))
        self.change_label.setStyleSheet(f"color: {ACCENT};")
        self.change_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        cash_layout.addWidget(self.change_label)

        layout.addWidget(cash_frame)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.remove_btn = QPushButton("🗑 Remove Item")
        self.remove_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.remove_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT};
                color: white;
                padding: 10px 16px;
                border-radius: 8px;
                font-family: Poppins;
                font-size: 10pt;
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
        self.remove_btn.clicked.connect(self.on_remove_from_cart)
        btn_layout.addWidget(self.remove_btn)

        self.complete_btn = PrimaryButton("Complete Sale", "✓")
        self.complete_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY};
                color: white;
                padding: 10px 16px;
                border-radius: 8px;
                font-family: Poppins;
                font-size: 10pt;
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
        self.complete_btn.clicked.connect(self.on_complete_sale)
        btn_layout.addWidget(self.complete_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def calculate_change(self):
        try:
            cash_text = self.cash_input.text().strip()

            if not cash_text or cash_text == '.' or cash_text == '-' or cash_text == '':
                self.change_label.setText("Change: ₱0.00")
                self.change_label.setStyleSheet(f"color: {ACCENT};")
                return

            cash_amount = float(cash_text)

            if self.current_total is None or self.current_total < 0:
                self.current_total = 0.0

            total_float = float(self.current_total)
            change = cash_amount - total_float

            if change >= 0:
                self.change_label.setText(f"Change: ₱{change:,.2f}")
                self.change_label.setStyleSheet(f"color: {ACCENT};")
            else:
                self.change_label.setText(f"Insufficient: ₱{abs(change):,.2f}")
                self.change_label.setStyleSheet("color: #D32F2F;")

        except Exception as e:
            print(f"Error in calculate_change: {e}")
            self.change_label.setText("Change: ₱0.00")
            self.change_label.setStyleSheet(f"color: {ACCENT};")

    def on_complete_sale(self):
        self.complete_sale_signal.emit()

    def update_cart(self, cart, total):
        self.current_total = total
        self.cart_table.setRowCount(len(cart))
        for i, item in enumerate(cart):
            # Product name
            product_item = QTableWidgetItem(item.product.name)
            product_item.setForeground(QColor("#2c3e50"))
            product_item.setFont(QFont("Poppins", 10))
            self.cart_table.setItem(i, 0, product_item)

            # Price
            price_item = QTableWidgetItem(f"₱{item.product.price:,.2f}")
            price_item.setForeground(QColor("#006D77"))
            price_item.setFont(QFont("Poppins", 10, QFont.Weight.Bold))
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.cart_table.setItem(i, 1, price_item)

            # Quantity
            qty_item = QTableWidgetItem(str(item.quantity))
            qty_item.setForeground(QColor("#2c3e50"))
            qty_item.setFont(QFont("Poppins", 10))
            qty_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.cart_table.setItem(i, 2, qty_item)

            # Total
            total_item = QTableWidgetItem(f"₱{item.get_total():,.2f}")
            total_item.setForeground(QColor("#006D77"))
            total_item.setFont(QFont("Poppins", 10, QFont.Weight.Bold))
            total_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.cart_table.setItem(i, 3, total_item)

        self.total_label.setText(f"Total: ₱{total:,.2f}")
        self.calculate_change()

    def on_remove_from_cart(self):
        row = self.cart_table.currentRow()
        if row >= 0:
            self.remove_from_cart_signal.emit(row)

    def clear_cash_input(self):
        self.cash_input.clear()
        self.change_label.setText("Change: ₱0.00")
        self.change_label.setStyleSheet(f"color: {ACCENT};")

    def get_cash_amount(self):
        try:
            cash_text = self.cash_input.text().strip()
            if not cash_text or cash_text == '.' or cash_text == '-':
                return None
            return float(cash_text)
        except (ValueError, TypeError):
            return None

    def get_current_total(self):
        return self.current_total