from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from View.components import *
from View.posView.cartView import cartView


class mainPosView(QWidget):
    add_to_cart_signal = pyqtSignal(str, int)  # product_id (str), quantity (int)
    remove_from_cart_signal = pyqtSignal(int)
    complete_sale_signal = pyqtSignal()
    logout_signal = pyqtSignal()
    back_to_admin_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.is_admin_mode = False
        self.cart_view = cartView()
        self.init_ui()

    def set_admin_mode(self, is_admin):
        """Show or hide the back to admin button based on user role"""
        self.is_admin_mode = is_admin
        self.back_to_admin_btn.setVisible(is_admin)

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # Header - WHITE background
        header_frame = HeaderFrame()
        header_layout = QHBoxLayout(header_frame)

        # Logo and title
        logo_label = QLabel()
        pixmap = QPixmap(r"C:\Users\kervy\Documents\Coding\T360Project\View\icons\T360logo.png")
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(45, 45, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(logo_label)

        header = QLabel("Point of Sale")
        header.setFont(QFont("Poppins", 24, QFont.Weight.Bold))
        header.setStyleSheet(f"color: {PRIMARY};")  # Teal color, readable on white
        header_layout.addWidget(header)
        header_layout.addStretch()

        # Back to Admin button
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

        # Logout button
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

        # Content layout
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # Products section (LEFT) - 60%
        products_frame = CardFrame()
        products_layout = QVBoxLayout(products_frame)
        products_layout.setContentsMargins(20, 20, 20, 20)
        products_layout.setSpacing(15)

        products_layout.addWidget(SectionLabel("Available Products", 18))

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

        # Cart section (RIGHT) - 40%
        self.cart_view.remove_from_cart_signal.connect(self.remove_from_cart_signal.emit)
        self.cart_view.complete_sale_signal.connect(self.complete_sale_signal.emit)
        content_layout.addWidget(self.cart_view, 40)

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

    def update_products(self, products):
        """
        Update products display
        NEW: Filters out products with 0 stock (only shows available items)
        """
        # ✅ FILTER: Only show products with stock > 0
        available_products = [p for p in products if p.stock > 0]

        self.products_table.setRowCount(len(available_products))

        for i, product in enumerate(available_products):
            # ID - Uses product_id (PR#####)
            id_item = QTableWidgetItem(str(product.product_id))
            id_item.setFont(QFont("Poppins", 9, QFont.Weight.Bold))
            id_item.setForeground(QColor("#006D77"))  # Teal color for product ID
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.products_table.setItem(i, 0, id_item)

            # Name
            name_item = QTableWidgetItem(product.name)
            name_item.setFont(QFont("Poppins", 10))
            self.products_table.setItem(i, 1, name_item)

            # Price
            price_item = QTableWidgetItem(f"₱{product.price:,.2f}")
            price_item.setFont(QFont("Poppins", 10, QFont.Weight.Bold))
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.products_table.setItem(i, 2, price_item)

            # Stock - Add visual indicator for low stock
            stock_item = QTableWidgetItem(str(product.stock))
            stock_item.setFont(QFont("Poppins", 10, QFont.Weight.Bold))
            stock_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            # Color code based on stock level
            if product.stock <= 5:
                stock_item.setForeground(QColor("#D32F2F"))  # Red for low stock
            elif product.stock <= 10:
                stock_item.setForeground(QColor("#F57C00"))  # Orange for medium stock
            else:
                stock_item.setForeground(QColor("#2E7D32"))  # Green for good stock

            self.products_table.setItem(i, 3, stock_item)

            # Quantity input - MUCH BIGGER and easier to click
            qty_input = QLineEdit()
            qty_input.setText("1")
            qty_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
            qty_input.setValidator(QIntValidator(1, max(1, product.stock)))
            qty_input.setMinimumWidth(120)  # Much wider
            qty_input.setMinimumHeight(45)  # Much taller - easy to click
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

            # Center the input widget
            container = QWidget()
            container_layout = QHBoxLayout(container)
            container_layout.addWidget(qty_input)
            container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            container_layout.setContentsMargins(0, 0, 0, 0)
            self.products_table.setCellWidget(i, 4, container)

        # Set column widths
        self.products_table.setColumnWidth(0, 80)  # Wider for PR##### format
        self.products_table.setColumnWidth(2, 120)
        self.products_table.setColumnWidth(3, 80)
        self.products_table.setColumnWidth(4, 150)  # Wider column for bigger input

        # Make rows taller to accommodate bigger input
        for row in range(self.products_table.rowCount()):
            self.products_table.setRowHeight(row, 55)

        # Show message if no products available
        if len(available_products) == 0:
            self.show_no_products_message()

    def show_no_products_message(self):
        """Display a message when there are no products in stock"""
        # Clear the table
        self.products_table.setRowCount(1)

        # Merge all columns for the message
        self.products_table.setSpan(0, 0, 1, 5)

        # Create message item
        message_item = QTableWidgetItem("No products available in stock")
        message_item.setFont(QFont("Poppins", 12, QFont.Weight.Bold))
        message_item.setForeground(QColor("#757575"))
        message_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        message_item.setFlags(Qt.ItemFlag.NoItemFlags)  # Make it non-selectable

        self.products_table.setItem(0, 0, message_item)
        self.products_table.setRowHeight(0, 100)

    def update_cart(self, cart, total):
        """Delegate to CartView"""
        self.cart_view.update_cart(cart, total)

    def highlight_selected_row(self):
        """Highlight the entire row including widget cells when selected"""
        # Reset all row backgrounds first
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

        # Highlight selected row
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
            # Check if this is the "no products" message row
            if self.products_table.rowSpan(row, 0) > 1:
                QMessageBox.information(self, "No Products", "There are no products available in stock.")
                return

            # Get product_id as string (e.g., "PR00001")
            product_id = self.products_table.item(row, 0).text()
            qty_widget = self.products_table.cellWidget(row, 4)
            qty_input = qty_widget.findChild(QLineEdit)
            quantity = int(qty_input.text()) if qty_input and qty_input.text() else 1

            # Debug print (optional - remove later)
            print(f"Adding to cart: product_id={product_id} (type: {type(product_id)}), quantity={quantity}")

            self.add_to_cart_signal.emit(product_id, quantity)
        else:
            QMessageBox.warning(self, "No Selection", "Please select a product first.")