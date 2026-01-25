from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont, QColor
from View.colors import *
from View.components import *  # Import reusable components


class ProductManagementTab(QWidget):
    """Product Management tab - add, delete, and search products"""

    add_product_signal = pyqtSignal(str, float, int)
    delete_product_signal = pyqtSignal(int)
    search_products_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # Left side - Add Product (25%)
        product_frame = CardFrame()
        product_layout = QVBoxLayout(product_frame)
        product_layout.setContentsMargins(20, 25, 20, 25)
        product_layout.setSpacing(15)

        product_layout.addWidget(SectionLabel("Add New Product"))
        product_layout.addWidget(SubtitleLabel("Fill in the details below"))

        # Form fields
        product_layout.addWidget(FieldLabel("Product Name"))
        self.product_name = StyledInput("Enter product name")
        product_layout.addWidget(self.product_name)

        product_layout.addWidget(FieldLabel("Price (₱)"))
        self.product_price = StyledInput("0.00")
        product_layout.addWidget(self.product_price)

        product_layout.addWidget(FieldLabel("Stock Quantity"))
        self.product_stock = QSpinBox()
        self.product_stock.setRange(0, 10000)
        self.product_stock.setPrefix("Stock: ")
        self.product_stock.setStyleSheet("""
            QSpinBox {
                font-family: Poppins; 
                font-size: 10pt;
                color: black; 
                padding: 10px 12px; 
                background-color: #F8FAFB; 
                border: 2px solid #E1E8ED; 
                border-radius: 8px;
            }
            QSpinBox:focus {
                border: 2px solid #006D77;
                background-color: white;
            }
        """)
        product_layout.addWidget(self.product_stock)

        add_btn = PrimaryButton("Add Product", "✓")
        add_btn.clicked.connect(self.on_add_product)
        product_layout.addWidget(add_btn)
        product_layout.addStretch()

        # Right side - Manage Products (75%)
        view_frame = CardFrame()
        view_layout = QVBoxLayout(view_frame)
        view_layout.setContentsMargins(25, 25, 25, 25)
        view_layout.setSpacing(15)

        view_layout.addWidget(SectionLabel("Manage Products", 18))

        self.search_input = SearchInput("🔍 Search products by name...")
        self.search_input.textChanged.connect(
            lambda: self.search_products_signal.emit(self.search_input.text()))
        view_layout.addWidget(self.search_input)

        self.products_table = StyledTable(5, ["ID", "Product Name", "Price", "Stock", "Actions"])
        self.products_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        view_layout.addWidget(self.products_table)

        main_layout.addWidget(product_frame, 25)
        main_layout.addWidget(view_frame, 75)

    def on_add_product(self):
        name = self.product_name.text().strip()
        try:
            price = float(self.product_price.text())
            stock = self.product_stock.value()
            if name and price > 0:
                self.add_product_signal.emit(name, price, stock)
                self.product_name.clear()
                self.product_price.clear()
                self.product_stock.setValue(0)
            else:
                QMessageBox.warning(self, "Invalid Input", "Please enter a valid product name and price.")
        except ValueError:
            QMessageBox.warning(self, "Error", "Invalid price format. Please enter numbers only.")

    def update_products_table(self, products):
        """Update the products table display"""
        self.products_table.setRowCount(len(products))
        for i, product in enumerate(products):
            # ID
            id_item = QTableWidgetItem(str(product.id))
            id_item.setForeground(QColor("#2c3e50"))
            id_item.setFont(QFont("Poppins", 10, QFont.Weight.Medium))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.products_table.setItem(i, 0, id_item)

            # Name
            name_item = QTableWidgetItem(product.name)
            name_item.setForeground(QColor("#2c3e50"))
            name_item.setFont(QFont("Poppins", 10))
            self.products_table.setItem(i, 1, name_item)

            # Price
            price_item = QTableWidgetItem(f"₱{product.price:,.2f}")
            price_item.setForeground(QColor("#006D77"))
            price_item.setFont(QFont("Poppins", 10, QFont.Weight.Bold))
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.products_table.setItem(i, 2, price_item)

            # Stock
            stock_item = QTableWidgetItem(str(product.stock))
            stock_item.setForeground(QColor("#2c3e50"))
            stock_item.setFont(QFont("Poppins", 10))
            stock_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.products_table.setItem(i, 3, stock_item)

            # Delete button
            delete_btn = DeleteButton()
            delete_btn.clicked.connect(lambda checked, pid=product.id: self.delete_product_signal.emit(pid))

            btn_container = QWidget()
            btn_layout = QHBoxLayout(btn_container)
            btn_layout.addWidget(delete_btn)
            btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            btn_layout.setContentsMargins(5, 5, 5, 5)
            self.products_table.setCellWidget(i, 4, btn_container)

        self.products_table.setColumnWidth(0, 60)
        self.products_table.setColumnWidth(2, 120)
        self.products_table.setColumnWidth(3, 80)
        self.products_table.setColumnWidth(4, 120)