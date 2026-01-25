from datetime import datetime
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from View.colors import *
from View.components import *
from .metricCard import MetricCard
from .productRankItem import ProductRankItem


class OverviewTab(QWidget):
    """Overview tab - displays dashboard metrics and statistics"""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # Header
        header = SectionLabel("Dashboard Overview", 24)
        main_layout.addWidget(header)

        # Metrics Row
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(15)

        self.monthly_sales_card = MetricCard("Monthly Sales", "₱0.00", "This month", PRIMARY)
        self.yearly_sales_card = MetricCard("Yearly Sales", "₱0.00", "This year", "#00796B")
        self.total_transactions_card = MetricCard("Transactions", "0", "All time", "#0277BD")
        self.avg_sale_card = MetricCard("Avg. Sale", "₱0.00", "Per transaction", "#7B1FA2")

        metrics_layout.addWidget(self.monthly_sales_card)
        metrics_layout.addWidget(self.yearly_sales_card)
        metrics_layout.addWidget(self.total_transactions_card)
        metrics_layout.addWidget(self.avg_sale_card)

        main_layout.addLayout(metrics_layout)

        # Content Row
        content_layout = QHBoxLayout()
        content_layout.setSpacing(15)

        # Top Products Section
        top_products_container = CardFrame()
        top_products_layout = QVBoxLayout(top_products_container)
        top_products_layout.setContentsMargins(25, 20, 25, 20)
        top_products_layout.setSpacing(15)

        top_products_title = QLabel("🏆 Top 5 Best Sellers")
        top_products_title.setFont(QFont("Poppins", 16, QFont.Weight.Bold))
        top_products_title.setStyleSheet(f"color: {PRIMARY};")
        top_products_layout.addWidget(top_products_title)

        # Container for top products list
        self.top_products_widget = QWidget()
        self.top_products_list_layout = QVBoxLayout(self.top_products_widget)
        self.top_products_list_layout.setSpacing(10)
        self.top_products_list_layout.setContentsMargins(0, 0, 0, 0)

        scroll_area = QScrollArea()
        scroll_area.setWidget(self.top_products_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        top_products_layout.addWidget(scroll_area)

        content_layout.addWidget(top_products_container, 3)

        # Inventory Status Section
        stock_container = CardFrame()
        stock_layout = QVBoxLayout(stock_container)
        stock_layout.setContentsMargins(25, 20, 25, 20)
        stock_layout.setSpacing(15)

        stock_title = QLabel("📦 Inventory Status")
        stock_title.setFont(QFont("Poppins", 16, QFont.Weight.Bold))
        stock_title.setStyleSheet(f"color: {PRIMARY};")
        stock_layout.addWidget(stock_title)

        # Stock metrics
        self.total_stock_label = QLabel("Total Items: 0")
        self.total_stock_label.setFont(QFont("Poppins", 13))
        self.total_stock_label.setStyleSheet("color: #2c3e50; padding: 10px; background-color: #F8FAFB; border-radius: 8px;")
        stock_layout.addWidget(self.total_stock_label)

        self.low_stock_label = QLabel("⚠️ Low Stock Items: 0")
        self.low_stock_label.setFont(QFont("Poppins", 13))
        self.low_stock_label.setStyleSheet("color: #F57C00; padding: 10px; background-color: #FFF3E0; border-radius: 8px;")
        stock_layout.addWidget(self.low_stock_label)

        self.out_of_stock_label = QLabel("❌ Out of Stock: 0")
        self.out_of_stock_label.setFont(QFont("Poppins", 13))
        self.out_of_stock_label.setStyleSheet("color: #D32F2F; padding: 10px; background-color: #FFEBEE; border-radius: 8px;")
        stock_layout.addWidget(self.out_of_stock_label)

        # Low stock products list
        low_stock_list_label = QLabel("Items Below 10 Units:")
        low_stock_list_label.setFont(QFont("Poppins", 12, QFont.Weight.Bold))
        low_stock_list_label.setStyleSheet("color: #2c3e50; margin-top: 15px;")
        stock_layout.addWidget(low_stock_list_label)

        self.low_stock_list = QListWidget()
        self.low_stock_list.setStyleSheet("""
            QListWidget {
                border: 2px solid #E8F4F5;
                border-radius: 8px;
                padding: 8px;
                background-color: #FAFAFA;
                font-family: Poppins;
                font-size: 11px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #EEEEEE;
                border-radius: 6px;
                margin: 2px;
            }
            QListWidget::item:hover {
                background-color: #FFF3E0;
            }
        """)
        stock_layout.addWidget(self.low_stock_list)

        content_layout.addWidget(stock_container, 2)

        main_layout.addLayout(content_layout)
        main_layout.addStretch()

    def update_overview(self, transactions, products):
        """Update all overview data"""
        try:
            now = datetime.now()
            month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            year_start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

            # Calculate sales
            monthly_sales = 0
            yearly_sales = 0

            for t in transactions:
                try:
                    if hasattr(t, 'created_at') and t.created_at:
                        trans_date = t.created_at
                    elif hasattr(t, 'date') and t.date:
                        trans_date = datetime.strptime(t.date, "%m-%d-%Y %I:%M %p")
                    else:
                        monthly_sales += t.total_amount
                        yearly_sales += t.total_amount
                        continue

                    if trans_date >= month_start:
                        monthly_sales += t.total_amount
                    if trans_date >= year_start:
                        yearly_sales += t.total_amount
                except (ValueError, AttributeError):
                    monthly_sales += t.total_amount
                    yearly_sales += t.total_amount

            # Total transactions and average
            total_transactions = len(transactions)
            avg_sale = sum(t.total_amount for t in transactions) / total_transactions if total_transactions > 0 else 0

            # Update metric cards
            self.monthly_sales_card.update_value(f"₱{monthly_sales:,.2f}")
            self.yearly_sales_card.update_value(f"₱{yearly_sales:,.2f}")
            self.total_transactions_card.update_value(str(total_transactions))
            self.avg_sale_card.update_value(f"₱{avg_sale:,.2f}")

            # Top Products
            product_sales = {}
            try:
                for transaction in transactions:
                    for item in transaction.items:
                        if isinstance(item, dict):
                            product_name = item.get('product_name', item.get('product', {}).get('name', 'Unknown'))
                            quantity = item.get('quantity', 0)
                        else:
                            product_name = getattr(item, 'product_name', 'Unknown')
                            quantity = getattr(item, 'quantity', 0)

                        product_sales[product_name] = product_sales.get(product_name, 0) + quantity
            except Exception as e:
                print(f"Error calculating top products: {e}")

            # Get top 5 products
            top_products = sorted(product_sales.items(), key=lambda x: x[1], reverse=True)[:5]

            # Clear existing product widgets
            while self.top_products_list_layout.count():
                child = self.top_products_list_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            # Add top products
            if top_products:
                colors = ["#00897B", "#1E88E5", "#7B1FA2", "#F57C00", "#E53935"]
                for idx, (product_name, quantity) in enumerate(top_products):
                    rank_item = ProductRankItem(idx + 1, product_name, quantity, colors[idx])
                    self.top_products_list_layout.addWidget(rank_item)
            else:
                no_data_label = QLabel("No sales data available")
                no_data_label.setFont(QFont("Poppins", 12))
                no_data_label.setStyleSheet("color: #999999; padding: 30px;")
                no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.top_products_list_layout.addWidget(no_data_label)

            self.top_products_list_layout.addStretch()

            # Inventory Status
            total_stock = sum(p.stock for p in products)
            low_stock_items = [p for p in products if 0 < p.stock <= 10]
            out_of_stock_items = [p for p in products if p.stock == 0]

            self.total_stock_label.setText(f"📊 Total Items in Stock: {total_stock}")
            self.low_stock_label.setText(f"⚠️ Low Stock Items (≤10): {len(low_stock_items)}")
            self.out_of_stock_label.setText(f"❌ Out of Stock: {len(out_of_stock_items)}")

            # Update low stock list
            self.low_stock_list.clear()
            for product in sorted(low_stock_items, key=lambda p: p.stock):
                self.low_stock_list.addItem(f"⚠ {product.name}: {product.stock} units")

            for product in out_of_stock_items:
                self.low_stock_list.addItem(f"❌ {product.name}: OUT OF STOCK")

            if not low_stock_items and not out_of_stock_items:
                self.low_stock_list.addItem("✅ All products are well stocked!")

        except Exception as e:
            print(f"Error updating overview: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.warning(self, "Error", f"Failed to update overview: {str(e)}")