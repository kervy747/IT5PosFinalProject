from datetime import datetime
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from View.colors import *
from View.components import *
from .statCard import StatCard
from .topProductCard import TopProductCard


class OverviewTab(QWidget):
    """Modern POS Dashboard Overview"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(24)

        # Removed header to save space

        # Stats Grid - 4 columns
        stats_grid = QGridLayout()
        stats_grid.setSpacing(16)

        self.revenue_card = StatCard("Today's Revenue", "₱0.00", "💰", color=PRIMARY)
        self.monthly_card = StatCard("Monthly Sales", "₱0.00", "📊", color="#00897B")
        self.transactions_card = StatCard("Transactions", "0", "🛒", color="#1E88E5")
        self.avg_card = StatCard("Avg. Transaction", "₱0.00", "💳", color="#7B1FA2")

        stats_grid.addWidget(self.revenue_card, 0, 0)
        stats_grid.addWidget(self.monthly_card, 0, 1)
        stats_grid.addWidget(self.transactions_card, 0, 2)
        stats_grid.addWidget(self.avg_card, 0, 3)

        main_layout.addLayout(stats_grid)

        # Content area with 2 columns
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # LEFT COLUMN - Top Products
        left_column = QVBoxLayout()
        left_column.setSpacing(16)

        # Top Products Section
        products_container = CardFrame()
        products_layout = QVBoxLayout(products_container)
        products_layout.setContentsMargins(24, 20, 24, 20)
        products_layout.setSpacing(16)

        products_header = QLabel("🏆 Top Selling Products")
        products_header.setFont(QFont("Poppins", 18, QFont.Weight.Bold))
        products_header.setStyleSheet(f"color: #000000; background: transparent;")
        products_layout.addWidget(products_header)

        # Scroll area for products
        self.products_widget = QWidget()
        self.products_list_layout = QVBoxLayout(self.products_widget)
        self.products_list_layout.setSpacing(10)
        self.products_list_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidget(self.products_widget)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #F0F0F0;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #CCCCCC;
                border-radius: 4px;
            }
        """)
        products_layout.addWidget(scroll)

        left_column.addWidget(products_container)
        content_layout.addLayout(left_column, 3)

        # RIGHT COLUMN - Inventory & Quick Stats
        right_column = QVBoxLayout()
        right_column.setSpacing(16)

        # Inventory Summary
        inventory_container = CardFrame()
        inventory_layout = QVBoxLayout(inventory_container)
        inventory_layout.setContentsMargins(24, 20, 24, 20)
        inventory_layout.setSpacing(16)

        inventory_header = QLabel("📦 Inventory Overview")
        inventory_header.setFont(QFont("Poppins", 18, QFont.Weight.Bold))
        inventory_header.setStyleSheet(f"color: #000000; background: transparent;")
        inventory_layout.addWidget(inventory_header)

        # Inventory metrics
        inv_grid = QGridLayout()
        inv_grid.setSpacing(12)

        self.total_products_widget = self._create_mini_stat("Total Products", "0", "#10B981")
        self.total_stock_widget = self._create_mini_stat("Total Stock", "0", PRIMARY)
        self.low_stock_widget = self._create_mini_stat("Low Stock", "0", "#F59E0B")
        self.out_stock_widget = self._create_mini_stat("Out of Stock", "0", "#EF4444")

        inv_grid.addWidget(self.total_products_widget, 0, 0)
        inv_grid.addWidget(self.total_stock_widget, 0, 1)
        inv_grid.addWidget(self.low_stock_widget, 1, 0)
        inv_grid.addWidget(self.out_stock_widget, 1, 1)

        inventory_layout.addLayout(inv_grid)

        # Alert list
        alert_header = QLabel("⚠️ Stock Alerts")
        alert_header.setFont(QFont("Poppins", 13, QFont.Weight.Bold))
        alert_header.setStyleSheet(f"color: #000000; margin-top: 8px; background: transparent;")
        inventory_layout.addWidget(alert_header)

        self.alert_list = QListWidget()
        self.alert_list.setStyleSheet(f"""
            QListWidget {{
                border: 1px solid {BACKGROUND};
                border-radius: 10px;
                padding: 8px;
                background-color: {BACKGROUND};
                font-family: Poppins;
                font-size: 11px;
                color: black;
            }}
            QListWidget::item {{
                padding: 10px;
                border-radius: 6px;
                margin: 2px 0;
                background-color: {WHITE};
                color: black;
            }}
            QListWidget::item:hover {{
                background-color: #FFF7ED;
            }}
        """)
        self.alert_list.setMaximumHeight(280)
        inventory_layout.addWidget(self.alert_list)

        right_column.addWidget(inventory_container)
        content_layout.addLayout(right_column, 2)

        main_layout.addLayout(content_layout)

    def _create_mini_stat(self, label, value, color):
        """Create mini stat widget"""
        container = QFrame()
        container.setStyleSheet(f"""
            QFrame {{
                background-color: {WHITE};
                border-radius: 10px;
                border-left: 4px solid {color};
                border: 1px solid {BACKGROUND};
            }}
        """)
        container.setMinimumHeight(70)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(4)

        title = QLabel(label)
        title.setFont(QFont("Poppins", 10, QFont.Weight.Medium))
        title.setStyleSheet(f"color: #000000; border: none; background: transparent;")
        layout.addWidget(title)

        val = QLabel(value)
        val.setFont(QFont("Poppins", 20, QFont.Weight.Bold))
        val.setStyleSheet(f"color: {color}; border: none; background: transparent;")
        val.setObjectName(f"{label.replace(' ', '_').lower()}_value")
        layout.addWidget(val)

        return container

    def update_overview(self, transactions, products):
        """Update dashboard with latest data"""
        try:
            now = datetime.now()
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

            # Calculate revenue
            today_revenue = 0
            monthly_revenue = 0
            total_transactions = len(transactions)

            for t in transactions:
                try:
                    if hasattr(t, 'created_at') and t.created_at:
                        trans_date = t.created_at
                    elif hasattr(t, 'date') and t.date:
                        trans_date = datetime.strptime(t.date, "%m-%d-%Y %I:%M %p")
                    else:
                        monthly_revenue += t.total_amount
                        continue

                    if trans_date >= today_start:
                        today_revenue += t.total_amount
                    if trans_date >= month_start:
                        monthly_revenue += t.total_amount
                except:
                    monthly_revenue += t.total_amount

            avg_transaction = sum(
                t.total_amount for t in transactions) / total_transactions if total_transactions > 0 else 0

            # Update stat cards
            self.revenue_card.update_value(f"₱{today_revenue:,.2f}")
            self.monthly_card.update_value(f"₱{monthly_revenue:,.2f}")
            self.transactions_card.update_value(str(total_transactions))
            self.avg_card.update_value(f"₱{avg_transaction:,.2f}")

            # Calculate top products with revenue
            product_data = {}
            for transaction in transactions:
                for item in transaction.items:
                    if isinstance(item, dict):
                        product_name = item.get('product_name', 'Unknown')
                        quantity = item.get('quantity', 0)
                        price = item.get('price', 0)
                    else:
                        product_name = getattr(item, 'product_name', 'Unknown')
                        quantity = getattr(item, 'quantity', 0)
                        price = getattr(item, 'price', 0)

                    if product_name not in product_data:
                        product_data[product_name] = {'quantity': 0, 'revenue': 0}
                    product_data[product_name]['quantity'] += quantity
                    product_data[product_name]['revenue'] += quantity * price

            # Sort by revenue
            top_products = sorted(product_data.items(), key=lambda x: x[1]['revenue'], reverse=True)[:5]

            # Clear and update products list
            while self.products_list_layout.count():
                child = self.products_list_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            if top_products:
                for idx, (name, data) in enumerate(top_products):
                    card = TopProductCard(idx + 1, name, data['quantity'], data['revenue'])
                    self.products_list_layout.addWidget(card)
            else:
                no_data = QLabel("No sales data available yet")
                no_data.setFont(QFont("Poppins", 12))
                no_data.setStyleSheet(f"color: {TEXT_DARK}60; padding: 40px;")
                no_data.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.products_list_layout.addWidget(no_data)

            self.products_list_layout.addStretch()

            # Update inventory stats
            total_stock = sum(p.stock for p in products)
            low_stock = [p for p in products if 0 < p.stock <= 10]
            out_of_stock = [p for p in products if p.stock == 0]

            # Update mini stats
            self._update_mini_stat(self.total_products_widget, str(len(products)))
            self._update_mini_stat(self.total_stock_widget, str(total_stock))
            self._update_mini_stat(self.low_stock_widget, str(len(low_stock)))
            self._update_mini_stat(self.out_stock_widget, str(len(out_of_stock)))

            # Update alert list
            self.alert_list.clear()

            for product in sorted(out_of_stock, key=lambda p: p.name):
                self.alert_list.addItem(f"🔴 {product.name} - OUT OF STOCK")

            for product in sorted(low_stock, key=lambda p: p.stock):
                self.alert_list.addItem(f"🟡 {product.name} - {product.stock} units left")

            if not low_stock and not out_of_stock:
                self.alert_list.addItem("✅ All products are well stocked!")

        except Exception as e:
            print(f"Error updating overview: {e}")
            import traceback
            traceback.print_exc()

    def _update_mini_stat(self, widget, value):
        """Update mini stat value"""
        for child in widget.findChildren(QLabel):
            if child.objectName().endswith('_value'):
                child.setText(value)
                break