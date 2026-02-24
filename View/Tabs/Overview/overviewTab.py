import os
import subprocess
import platform
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap
from View.components import *
from .topProductCard import TopProductCard
from .barChartWidget import BarChartWidget
from .lineChartWidget import LineChartWidget
from report_generator import ReportGenerator


class OverviewTab(QWidget):
    def __init__(self, overview_controller):
        super().__init__()
        self.controller = overview_controller
        self._current_dashboard_data = None
        self._current_month_name = ""
        self._current_year = 0
        self._current_transactions = []
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(14)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)

        logo_label = QLabel()
        icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "Assets", "overviewLogo.svg")
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        header_layout.addWidget(logo_label)

        dashboard_title = QLabel("Dashboard Overview")
        dashboard_title.setFont(QFont("Poppins", 16, QFont.Weight.Bold))
        dashboard_title.setStyleSheet(f"color: {PRIMARY};")
        header_layout.addWidget(dashboard_title)

        header_layout.addStretch()

        self.month_selector = MonthYearSelector(start_year=2020)
        self.month_selector.setMaximumWidth(350)
        self.month_selector.month_changed.connect(self.on_month_changed)
        header_layout.addWidget(self.month_selector)

        export_btn = QPushButton("🖨 Export PDF")
        export_btn.setFont(QFont("Poppins", 9, QFont.Weight.Medium))
        export_btn.setFixedHeight(36)
        export_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        export_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY};
                color: white;
                border-radius: 8px;
                padding: 0 16px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #005f68;
            }}
            QPushButton:pressed {{
                background-color: #004f57;
            }}
        """)
        export_btn.clicked.connect(self.export_pdf)
        header_layout.addWidget(export_btn)

        main_layout.addLayout(header_layout)

        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(12)

        self.revenue_card = self._create_compact_stat("Today's Revenue", "₱0.00", "💰", PRIMARY)
        self.monthly_card = self._create_compact_stat("Monthly Sales", "₱0.00", "📊", "#00897B")
        self.avg_card = self._create_compact_stat("Avg. Transaction", "₱0.00", "💳", "#7B1FA2")

        stats_layout.addWidget(self.revenue_card[0])
        stats_layout.addWidget(self.monthly_card[0])
        stats_layout.addWidget(self.avg_card[0])

        main_layout.addLayout(stats_layout)

        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(14)

        bar_container = CardFrame()
        bar_layout = QVBoxLayout(bar_container)
        bar_layout.setContentsMargins(16, 12, 16, 12)
        bar_layout.setSpacing(6)

        bar_header = QLabel("📊 Daily Revenue (Last 7 Days)")
        bar_header.setFont(QFont("Poppins", 12, QFont.Weight.Bold))
        bar_header.setStyleSheet("color: #000000; background: transparent;")
        bar_layout.addWidget(bar_header)

        self.bar_chart = BarChartWidget()
        bar_layout.addWidget(self.bar_chart)
        charts_layout.addWidget(bar_container, 1)

        line_container = CardFrame()
        line_layout = QVBoxLayout(line_container)
        line_layout.setContentsMargins(16, 12, 16, 12)
        line_layout.setSpacing(6)

        line_header = QLabel("📈 Monthly Revenue Trend")
        line_header.setFont(QFont("Poppins", 12, QFont.Weight.Bold))
        line_header.setStyleSheet("color: #000000; background: transparent;")
        line_layout.addWidget(line_header)

        self.line_chart = LineChartWidget()
        line_layout.addWidget(self.line_chart)
        charts_layout.addWidget(line_container, 1)

        main_layout.addLayout(charts_layout, 1)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(14)

        products_container = CardFrame()
        products_layout = QVBoxLayout(products_container)
        products_layout.setContentsMargins(16, 14, 16, 14)
        products_layout.setSpacing(10)

        products_header = QLabel("🏆 Top Selling Products")
        products_header.setFont(QFont("Poppins", 14, QFont.Weight.Bold))
        products_header.setStyleSheet("color: #000000; background: transparent;")
        products_layout.addWidget(products_header)

        self.products_month_label = QLabel()
        self.products_month_label.setFont(QFont("Poppins", 9))
        self.products_month_label.setStyleSheet("color: #64748B; background: transparent;")
        products_layout.addWidget(self.products_month_label)

        self.products_widget = QWidget()
        self.products_widget.setStyleSheet("background: transparent;")
        self.products_list_layout = QVBoxLayout(self.products_widget)
        self.products_list_layout.setSpacing(8)
        self.products_list_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidget(self.products_widget)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea { border: none; background-color: transparent; }
            QScrollBar:vertical { border: none; background: #F0F0F0; width: 6px; border-radius: 3px; }
            QScrollBar::handle:vertical { background: #CCCCCC; border-radius: 3px; }
        """)
        products_layout.addWidget(scroll)
        content_layout.addWidget(products_container, 1)

        inventory_container = CardFrame()
        inventory_layout = QVBoxLayout(inventory_container)
        inventory_layout.setContentsMargins(16, 14, 16, 14)
        inventory_layout.setSpacing(10)

        inventory_header = QLabel("📦 Inventory Overview")
        inventory_header.setFont(QFont("Poppins", 14, QFont.Weight.Bold))
        inventory_header.setStyleSheet("color: #000000; background: transparent;")
        inventory_layout.addWidget(inventory_header)

        inv_panels_layout = QHBoxLayout()
        inv_panels_layout.setSpacing(12)

        inv_grid = QGridLayout()
        inv_grid.setSpacing(8)
        inv_grid.setColumnStretch(0, 1)
        inv_grid.setColumnStretch(1, 1)
        inv_grid.setRowStretch(0, 1)
        inv_grid.setRowStretch(1, 1)

        self.total_products_widget = self._create_mini_stat("Total Products", "0", "#10B981")
        self.total_stock_widget = self._create_mini_stat("Total Stock", "0", PRIMARY)
        self.low_stock_widget = self._create_mini_stat("Low Stock", "0", "#F59E0B")
        self.out_stock_widget = self._create_mini_stat("Out of Stock", "0", "#EF4444")

        for widget in [self.total_products_widget, self.total_stock_widget,
                       self.low_stock_widget, self.out_stock_widget]:
            widget.setFixedHeight(75)

        inv_grid.addWidget(self.total_products_widget, 0, 0)
        inv_grid.addWidget(self.total_stock_widget, 0, 1)
        inv_grid.addWidget(self.low_stock_widget, 1, 0)
        inv_grid.addWidget(self.out_stock_widget, 1, 1)

        inv_panels_layout.addLayout(inv_grid, 1)

        alerts_panel_layout = QVBoxLayout()
        alerts_panel_layout.setSpacing(6)

        alert_header = QLabel("⚠️ Stock Alerts")
        alert_header.setFont(QFont("Poppins", 11, QFont.Weight.Bold))
        alert_header.setStyleSheet("color: #000000; background: transparent;")
        alerts_panel_layout.addWidget(alert_header)

        self.alert_list = QListWidget()
        self.alert_list.setStyleSheet(f"""
            QListWidget {{
                border: 1px solid {BACKGROUND};
                border-radius: 8px;
                padding: 6px;
                background-color: {BACKGROUND};
                font-family: Poppins;
                font-size: 10px;
                color: black;
            }}
            QListWidget::item {{
                padding: 8px;
                border-radius: 6px;
                margin: 2px 0;
                background-color: {WHITE};
                color: black;
            }}
            QListWidget::item:hover {{ background-color: #FFF7ED; }}
        """)
        alerts_panel_layout.addWidget(self.alert_list)

        inv_panels_layout.addLayout(alerts_panel_layout, 1)

        inventory_layout.addLayout(inv_panels_layout)

        content_layout.addWidget(inventory_container, 1)
        main_layout.addLayout(content_layout, 1)

    def _create_compact_stat(self, label, value, icon, color):
        container = QFrame()
        container.setStyleSheet(f"""
            QFrame {{
                background-color: {WHITE};
                border-radius: 12px;
                border: none;
            }}
        """)
        container.setFixedHeight(80)

        layout = QHBoxLayout(container)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(12)

        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Segoe UI Emoji", 22))
        icon_label.setStyleSheet("background: transparent;")
        layout.addWidget(icon_label)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)

        title_label = QLabel(label)
        title_label.setFont(QFont("Poppins", 9, QFont.Weight.Medium))
        title_label.setStyleSheet("color: #64748B; background: transparent;")
        text_layout.addWidget(title_label)

        value_label = QLabel(value)
        value_label.setFont(QFont("Poppins", 16, QFont.Weight.Bold))
        value_label.setStyleSheet(f"color: {color}; background: transparent;")
        value_label.setObjectName(f"compact_value_{label.replace(' ', '_').lower()}")
        text_layout.addWidget(value_label)

        layout.addLayout(text_layout)
        layout.addStretch()

        return container, value_label

    def _create_mini_stat(self, label, value, color):
        container = QFrame()
        container.setStyleSheet(f"""
            QFrame {{
                background-color: {WHITE};
                border-radius: 8px;
                border: 1px solid {BACKGROUND};
            }}
        """)
        container.setMinimumHeight(60)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(2)

        title = QLabel(label)
        title.setFont(QFont("Poppins", 9, QFont.Weight.Medium))
        title.setStyleSheet("color: #000000; border: none; background: transparent;")
        layout.addWidget(title)

        val = QLabel(value)
        val.setFont(QFont("Poppins", 16, QFont.Weight.Bold))
        val.setStyleSheet(f"color: {color}; border: none; background: transparent;")
        val.setObjectName(f"{label.replace(' ', '_').lower()}_value")
        layout.addWidget(val)

        return container

    def on_month_changed(self, month, year):
        self.update_overview(month, year)

    def update_overview(self, selected_month=None, selected_year=None):
        try:
            self.month_selector.set_available_years(self.controller.data_model.transactions)

            dashboard_data = self.controller.get_dashboard_data(selected_month, selected_year)

            months = ["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December"]
            month_name = months[dashboard_data['selected_month'] - 1]
            self.products_month_label.setText(f"For {month_name} {dashboard_data['selected_year']}")

            self._current_dashboard_data = dashboard_data
            self._current_month_name = month_name
            self._current_year = dashboard_data['selected_year']
            self._current_transactions = self._get_month_transactions(
                dashboard_data['selected_month'], dashboard_data['selected_year']
            )

            self._update_revenue_metrics(dashboard_data['revenue_metrics'])
            self._update_top_products(dashboard_data['top_products'])
            self._update_inventory_stats(dashboard_data['inventory_stats'])
            self._update_stock_alerts(dashboard_data['stock_alerts'])
            self._update_charts(dashboard_data['selected_month'], dashboard_data['selected_year'])

        except Exception as e:
            print(f"Error updating overview: {e}")
            import traceback
            traceback.print_exc()

    def _get_month_transactions(self, month, year):
        from datetime import datetime as dt
        transactions = self.controller.data_model.transactions
        filtered = []
        for t in transactions:
            try:
                if hasattr(t, 'created_at') and t.created_at:
                    trans_date = t.created_at
                elif hasattr(t, 'date') and t.date:
                    trans_date = dt.strptime(t.date, "%m-%d-%Y %I:%M %p")
                else:
                    continue
                if trans_date.month == month and trans_date.year == year:
                    filtered.append(t)
            except Exception:
                continue
        return filtered

    def export_pdf(self):
        if not self._current_dashboard_data:
            QMessageBox.warning(self, "No Data", "Please wait for the dashboard to load before exporting.")
            return

        try:
            generator = ReportGenerator()
            filepath = generator.generate(
                self._current_dashboard_data,
                self._current_month_name,
                self._current_year,
                self._current_transactions
            )

            msg = QMessageBox(self)
            msg.setWindowTitle("Report Exported")
            msg.setText(f"PDF report saved successfully!")
            msg.setInformativeText(filepath)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Open)
            msg.setDefaultButton(QMessageBox.StandardButton.Open)
            result = msg.exec()

            if result == QMessageBox.StandardButton.Open:
                system = platform.system()
                if system == "Windows":
                    os.startfile(filepath)
                elif system == "Darwin":
                    subprocess.call(["open", filepath])
                else:
                    subprocess.call(["xdg-open", filepath])

        except Exception as e:
            QMessageBox.critical(self, "Export Failed", f"Could not generate PDF:\n{str(e)}")

    def _update_charts(self, selected_month, selected_year):
        try:
            daily_data = self.controller.get_revenue_trend(days=7)
            sorted_days = sorted(daily_data.items())
            bar_labels = [d[5:] for d, _ in sorted_days]
            bar_values = [v for _, v in sorted_days]
            self.bar_chart.set_data(bar_labels, bar_values)
        except Exception as e:
            print(f"Error updating bar chart: {e}")

        try:
            months_short = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            monthly_labels = []
            monthly_values = []

            for m in range(1, selected_month + 1):
                data = self.controller.get_dashboard_data(m, selected_year)
                monthly_labels.append(months_short[m - 1])
                monthly_values.append(data['revenue_metrics']['monthly_revenue'])

            self.line_chart.set_data(monthly_labels, monthly_values)
        except Exception as e:
            print(f"Error updating line chart: {e}")

    def _update_revenue_metrics(self, metrics):
        self.revenue_card[1].setText(f"₱{metrics['today_revenue']:,.2f}")
        self.monthly_card[1].setText(f"₱{metrics['monthly_revenue']:,.2f}")
        self.avg_card[1].setText(f"₱{metrics['avg_transaction']:,.2f}")

    def _update_top_products(self, top_products):
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
            no_data.setFont(QFont("Poppins", 11))
            no_data.setStyleSheet(f"color: {TEXT_DARK}60; padding: 30px; background: transparent;")
            no_data.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.products_list_layout.addWidget(no_data)

        self.products_list_layout.addStretch()

    def _update_inventory_stats(self, stats):
        self._update_mini_stat(self.total_products_widget, str(stats['total_products']))
        self._update_mini_stat(self.total_stock_widget, str(stats['total_stock']))
        self._update_mini_stat(self.low_stock_widget, str(stats['low_stock_count']))
        self._update_mini_stat(self.out_stock_widget, str(stats['out_of_stock_count']))

    def _update_stock_alerts(self, alerts):
        self.alert_list.clear()
        for alert in alerts:
            self.alert_list.addItem(f"{alert['icon']} {alert['message']}")

    def _update_mini_stat(self, widget, value):
        for child in widget.findChildren(QLabel):
            if child.objectName().endswith('_value'):
                child.setText(value)
                break