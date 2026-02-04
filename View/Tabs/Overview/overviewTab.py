from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from View.colors import *
from View.components import *
from .statCard import StatCard
from .topProductCard import TopProductCard


class OverviewTab(QWidget):
    """Modern POS Dashboard Overview - View Only (Pure View Component)"""

    def __init__(self, overview_controller):
        """
        Initialize the overview tab

        Args:
            overview_controller: Instance of OverviewController for business logic
        """
        super().__init__()
        self.controller = overview_controller
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(24)

        # Header with Month Selector
        header_layout = QHBoxLayout()
        header_layout.setSpacing(16)

        # Dashboard title
        dashboard_title = QLabel("📊 Dashboard Overview")
        dashboard_title.setFont(QFont("Poppins", 20, QFont.Weight.Bold))
        dashboard_title.setStyleSheet(f"color: {PRIMARY};")
        header_layout.addWidget(dashboard_title)

        header_layout.addStretch()

        # Month/Year selector (dropdown)
        self.month_selector = MonthYearSelector(start_year=2020)
        self.month_selector.setMaximumWidth(400)
        self.month_selector.month_changed.connect(self.on_month_changed)
        header_layout.addWidget(self.month_selector)

        main_layout.addLayout(header_layout)

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

        # Month indicator for top products
        self.products_month_label = QLabel()
        self.products_month_label.setFont(QFont("Poppins", 10))
        self.products_month_label.setStyleSheet("color: #64748B; background: transparent;")
        products_layout.addWidget(self.products_month_label)

        # Scroll area for products
        self.products_widget = QWidget()
        self.products_widget.setStyleSheet("background: transparent;")
        self.products_list_layout = QVBoxLayout(self.products_widget)
        self.products_list_layout.setSpacing(12)
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
        """
        Create mini stat widget

        Args:
            label: Label for the stat
            value: Initial value
            color: Color for the stat

        Returns:
            QFrame: The stat widget
        """
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

    def on_month_changed(self, month, year):
        """
        Handle month selection change

        Args:
            month: Selected month (1-12)
            year: Selected year
        """
        self.update_overview(month, year)

    def update_overview(self, selected_month=None, selected_year=None):
        """
        Update dashboard with latest data from controller

        Args:
            selected_month: Optional month to display (1-12)
            selected_year: Optional year to display
        """
        try:
            # Get all data from controller
            dashboard_data = self.controller.get_dashboard_data(
                selected_month, selected_year
            )

            # Update month label
            months = [
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ]
            month_name = months[dashboard_data['selected_month'] - 1]
            self.products_month_label.setText(
                f"For {month_name} {dashboard_data['selected_year']}"
            )

            # Update revenue metrics
            self._update_revenue_metrics(dashboard_data['revenue_metrics'])

            # Update top products
            self._update_top_products(dashboard_data['top_products'])

            # Update inventory stats
            self._update_inventory_stats(dashboard_data['inventory_stats'])

            # Update stock alerts
            self._update_stock_alerts(dashboard_data['stock_alerts'])

        except Exception as e:
            print(f"Error updating overview: {e}")
            import traceback
            traceback.print_exc()

    def _update_revenue_metrics(self, metrics):
        """
        Update revenue stat cards

        Args:
            metrics: Dictionary containing revenue metrics
        """
        self.revenue_card.update_value(f"₱{metrics['today_revenue']:,.2f}")
        self.monthly_card.update_value(f"₱{metrics['monthly_revenue']:,.2f}")
        self.transactions_card.update_value(str(metrics['monthly_transactions']))
        self.avg_card.update_value(f"₱{metrics['avg_transaction']:,.2f}")

    def _update_top_products(self, top_products):
        """
        Update top products list

        Args:
            top_products: List of (product_name, data_dict) tuples
        """
        # Clear existing products
        while self.products_list_layout.count():
            child = self.products_list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if top_products:
            for idx, (name, data) in enumerate(top_products):
                card = TopProductCard(idx + 1, name, data['quantity'], data['revenue'])
                self.products_list_layout.addWidget(card)
        else:
            no_data = QLabel("No sales data available for this month")
            no_data.setFont(QFont("Poppins", 12))
            no_data.setStyleSheet(f"color: {TEXT_DARK}60; padding: 40px; background: transparent;")
            no_data.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.products_list_layout.addWidget(no_data)

        self.products_list_layout.addStretch()

    def _update_inventory_stats(self, stats):
        """
        Update inventory statistics

        Args:
            stats: Dictionary containing inventory statistics
        """
        self._update_mini_stat(self.total_products_widget, str(stats['total_products']))
        self._update_mini_stat(self.total_stock_widget, str(stats['total_stock']))
        self._update_mini_stat(self.low_stock_widget, str(stats['low_stock_count']))
        self._update_mini_stat(self.out_stock_widget, str(stats['out_of_stock_count']))

    def _update_stock_alerts(self, alerts):
        """
        Update stock alerts list

        Args:
            alerts: List of alert dictionaries
        """
        self.alert_list.clear()

        for alert in alerts:
            self.alert_list.addItem(f"{alert['icon']} {alert['message']}")

    def _update_mini_stat(self, widget, value):
        """
        Update mini stat value

        Args:
            widget: The stat widget to update
            value: New value to display
        """
        for child in widget.findChildren(QLabel):
            if child.objectName().endswith('_value'):
                child.setText(value)
                break