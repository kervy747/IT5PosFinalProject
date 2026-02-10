from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from View.components import *
from View.posView.cartView import cartView
import os


class mainPosView(QWidget):
    add_to_cart_signal = pyqtSignal(str, int)
    remove_from_cart_signal = pyqtSignal(int)
    complete_sale_signal = pyqtSignal()
    logout_signal = pyqtSignal()
    back_to_admin_signal = pyqtSignal()
    search_product_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.is_admin_mode = False
        self.cart_view = cartView()
        self.all_products = []
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        header_frame = HeaderFrame()
        header_layout = QHBoxLayout(header_frame)

        logo_label = QLabel()
        pixmap = QPixmap(r"C:\Users\kervy\Documents\Coding\IT5FinalProject\Assets\T360logo.png")
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(45, 45, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(logo_label)

        header = QLabel("Point of Sale")
        header.setFont(QFont("Poppins", 24, QFont.Weight.Bold))
        header.setStyleSheet(f"color: {PRIMARY};")
        header_layout.addWidget(header)
        header_layout.addStretch()

        self.back_to_admin_btn = QPushButton("← Back to Admin")
        self.back_to_admin_btn.setFixedWidth(150)
        self.back_to_admin_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_to_admin_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY};
                color: white;
                padding: 10px 15px;
                border-radius: 8px;
                font-weight: bold;
                font-family: Poppins;
                font-size: 10pt;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #005662;
            }}
            QPushButton:pressed {{
                background-color: #004a54;
            }}
        """)
        self.back_to_admin_btn.clicked.connect(self.back_to_admin_signal.emit)
        self.back_to_admin_btn.setVisible(False)
        header_layout.addWidget(self.back_to_admin_btn)

        logout_btn = QPushButton("Logout")
        logout_btn.setFixedWidth(100)
        logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        logout_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT};
                color: white;
                padding: 10px 15px;
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
        logout_btn.clicked.connect(self.logout_signal.emit)
        header_layout.addWidget(logout_btn)

        main_layout.addWidget(header_frame)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        products_frame = CardFrame()
        products_layout = QVBoxLayout(products_frame)
        products_layout.setContentsMargins(20, 20, 20, 20)
        products_layout.setSpacing(15)

        products_layout.addWidget(SectionLabel("Available Products", 18))

        self.search_input = SearchInput("Search by Product ID or Name...")

        search_icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "Assets", "searchIcon.svg")
        if os.path.exists(search_icon_path):
            search_icon = QIcon(search_icon_path)
            search_action = QAction(search_icon, "", self.search_input)
            self.search_input.addAction(search_action, QLineEdit.ActionPosition.LeadingPosition)

        self.search_input.textChanged.connect(self.filter_products)

        products_layout.addWidget(self.search_input)

        self.products_table = StyledTable(5, ["ID", "Product Name", "Price", "Stock", "Quantity"])
        self.products_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.products_table.itemSelectionChanged.connect(self.highlight_selected_row)
        products_layout.addWidget(self.products_table)

        add_btn = PrimaryButton("Add to Cart", "🛒")
        add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY};
                color: white;
                padding: 12px 20px;
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
        add_btn.clicked.connect(self.on_add_to_cart)
        products_layout.addWidget(add_btn)

        content_layout.addWidget(products_frame, 60)

        self.cart_view.remove_from_cart_signal.connect(self.remove_from_cart_signal.emit)
        self.cart_view.complete_sale_signal.connect(self.complete_sale_signal.emit)
        content_layout.addWidget(self.cart_view, 40)

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

    def filter_products(self):
        search_text = self.search_input.text().strip().lower()

        if not search_text:
            self._display_products(self.all_products)
        else:
            filtered = [
                p for p in self.all_products
                if search_text in p.product_id.lower() or search_text in p.name.lower()
            ]
            self._display_products(filtered)

    def update_products(self, products):
        self.all_products = products
        self._display_products(products)

    def _display_products(self, products):
        self.products_table.clearSpans()
        self.products_table.setRowCount(len(products))

        for i, product in enumerate(products):
            id_item = QTableWidgetItem(str(product.product_id))
            id_item.setFont(QFont("Poppins", 9, QFont.Weight.Bold))
            id_item.setForeground(QColor("#006D77"))
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.products_table.setItem(i, 0, id_item)

            name_item = QTableWidgetItem(product.name)
            name_item.setFont(QFont("Poppins", 10))
            self.products_table.setItem(i, 1, name_item)

            price_item = QTableWidgetItem(f"₱{product.price:,.2f}")
            price_item.setFont(QFont("Poppins", 10, QFont.Weight.Bold))
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.products_table.setItem(i, 2, price_item)

            stock_item = QTableWidgetItem(str(product.stock))
            stock_item.setFont(QFont("Poppins", 10, QFont.Weight.Bold))
            stock_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            if product.stock <= 5:
                stock_item.setForeground(QColor("#D32F2F"))
            elif product.stock <= 10:
                stock_item.setForeground(QColor("#F57C00"))
            else:
                stock_item.setForeground(QColor("#2E7D32"))

            self.products_table.setItem(i, 3, stock_item)

            qty_input = QLineEdit()
            qty_input.setText("1")
            qty_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
            qty_input.setValidator(QIntValidator(1, max(1, product.stock)))
            qty_input.setMinimumWidth(120)
            qty_input.setMinimumHeight(45)
            qty_input.setStyleSheet("""
                QLineEdit {
                    color: black;
                    font-family: Poppins;
                    font-size: 14pt;
                    font-weight: bold;
                    background-color: #F8FAFB;
                    padding: 12px;
                    border: 3px solid #E1E8ED;
                    border-radius: 8px;
                }
                QLineEdit:focus {
                    border: 3px solid #006D77;
                    background-color: white;
                }
                QLineEdit:hover {
                    border: 3px solid #83C5BE;
                    background-color: white;
                    cursor: text;
                }
            """)

            container = QWidget()
            container_layout = QHBoxLayout(container)
            container_layout.addWidget(qty_input)
            container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            container_layout.setContentsMargins(0, 0, 0, 0)
            self.products_table.setCellWidget(i, 4, container)

        self.products_table.setColumnWidth(0, 80)
        self.products_table.setColumnWidth(2, 120)
        self.products_table.setColumnWidth(3, 80)
        self.products_table.setColumnWidth(4, 150)

        for row in range(self.products_table.rowCount()):
            self.products_table.setRowHeight(row, 55)

        if len(products) == 0:
            self.show_no_products_message()

    def show_no_products_message(self):
        self.products_table.setRowCount(1)
        self.products_table.setSpan(0, 0, 1, 5)

        message_item = QTableWidgetItem("No products found")
        message_item.setFont(QFont("Poppins", 12, QFont.Weight.Bold))
        message_item.setForeground(QColor("#757575"))
        message_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        message_item.setFlags(Qt.ItemFlag.NoItemFlags)

        self.products_table.setItem(0, 0, message_item)
        self.products_table.setRowHeight(0, 100)

    def update_cart(self, cart, total):
        self.cart_view.update_cart(cart, total)

    def highlight_selected_row(self):
        for row in range(self.products_table.rowCount()):
            qty_widget = self.products_table.cellWidget(row, 4)
            if qty_widget:
                qty_input = qty_widget.findChild(QLineEdit)
                if qty_input:
                    qty_input.setStyleSheet("""
                        QLineEdit {
                            color: black;
                            font-family: Poppins;
                            font-size: 14pt;
                            font-weight: bold;
                            background-color: #F8FAFB;
                            padding: 12px;
                            border: 3px solid #E1E8ED;
                            border-radius: 8px;
                        }
                        QLineEdit:focus {
                            border: 3px solid #006D77;
                            background-color: white;
                        }
                        QLineEdit:hover {
                            border: 3px solid #83C5BE;
                            background-color: white;
                            cursor: text;
                        }
                    """)

        selected_rows = self.products_table.selectedIndexes()
        if selected_rows:
            row = selected_rows[0].row()
            qty_widget = self.products_table.cellWidget(row, 4)
            if qty_widget:
                qty_input = qty_widget.findChild(QLineEdit)
                if qty_input:
                    qty_input.setStyleSheet("""
                        QLineEdit {
                            color: black;
                            font-family: Poppins;
                            font-size: 14pt;
                            font-weight: bold;
                            background-color: #83C5BE;
                            padding: 12px;
                            border: 3px solid #E1E8ED;
                            border-radius: 8px;
                        }
                        QLineEdit:focus {
                            border: 3px solid #006D77;
                            background-color: #83C5BE;
                        }
                        QLineEdit:hover {
                            border: 3px solid #83C5BE;
                            background-color: #83C5BE;
                            cursor: text;
                        }
                    """)

    def on_add_to_cart(self):
        row = self.products_table.currentRow()
        if row >= 0:
            if self.products_table.rowSpan(row, 0) > 1:
                QMessageBox.information(self, "No Products", "There are no products available.")
                return

            product_id = self.products_table.item(row, 0).text()
            qty_widget = self.products_table.cellWidget(row, 4)
            qty_input = qty_widget.findChild(QLineEdit)
            quantity = int(qty_input.text()) if qty_input and qty_input.text() else 1

            self.add_to_cart_signal.emit(product_id, quantity)
        else:
            QMessageBox.warning(self, "No Selection", "Please select a product first.")