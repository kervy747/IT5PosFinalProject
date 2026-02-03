from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTabWidget
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont, QPixmap
from View.colors import *
from View.Tabs.Overview.overviewTab import OverviewTab
from View.Tabs.Transaction.transactionsTab import TransactionsTab
from View.Tabs.userManagementTab import UserManagementTab
from View.Tabs.productManagementTab import ProductManagementTab
from Controller.overview_controller import OverviewController


class AdminTabbedView(QWidget):
    """Main admin interface container with tabbed navigation"""

    # Signals from all tabs
    logout_signal = pyqtSignal()

    # User management signals
    add_user_signal = pyqtSignal(str, str, str)
    delete_user_signal = pyqtSignal(str)
    search_users_signal = pyqtSignal(str)

    # Product management signals
    add_product_signal = pyqtSignal(str, float, int)
    delete_product_signal = pyqtSignal(str)
    search_products_signal = pyqtSignal(str)

    # Transaction signals (search only, no delete)
    search_transactions_signal = pyqtSignal(str)

    def __init__(self, data_model):
        super().__init__()
        self.data_model = data_model

        # Create overview controller
        self.overview_controller = OverviewController(data_model)

        self.init_ui()
        self._connect_tab_signals()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ==================== HEADER ====================
        header_widget = QWidget()
        header_widget.setStyleSheet(f"""
            QWidget {{
                background-color: white;
                border-bottom: 2px solid {ACCENT};
            }}
        """)
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(25, 15, 25, 15)

        # Logo and Title
        logo_title_layout = QHBoxLayout()
        logo_title_layout.setSpacing(12)

        logo_label = QLabel()
        pixmap = QPixmap(r"C:\Users\kervy\Documents\Coding\T360Project\View\icons\T360logo.png")
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(45, 45, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        logo_title_layout.addWidget(logo_label)

        title = QLabel("Admin Dashboard")
        title.setFont(QFont("Poppins", 20, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {PRIMARY};")
        logo_title_layout.addWidget(title)

        header_layout.addLayout(logo_title_layout)
        header_layout.addStretch()

        # Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.setFixedWidth(110)
        logout_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT};
                color: white;
                padding: 10px 16px;
                border-radius: 6px;
                font-family: Poppins;
                font-size: 13px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #6FAAA4;
            }}
            QPushButton:pressed {{
                background-color: #5A9489;
            }}
            QPushButton:focus {{
                outline: none;
                border: none;
            }}
        """)
        logout_btn.clicked.connect(self.logout_signal.emit)
        header_layout.addWidget(logout_btn)

        main_layout.addWidget(header_widget)

        # ==================== TAB WIDGET ====================
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                background-color: {BACKGROUND};
            }}
            QTabBar::tab {{
                background-color: #E0E0E0;
                color: #666666;
                padding: 12px 30px;
                margin-right: 2px;
                font-family: Poppins;
                font-size: 13px;
                font-weight: bold;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }}
            QTabBar::tab:selected {{
                background-color: {PRIMARY};
                color: white;
            }}
            QTabBar::tab:hover:!selected {{
                background-color: #BDBDBD;
                color: #333333;
            }}
        """)

        # Create tab instances (each from separate files)
        self.overview_tab = OverviewTab(self.overview_controller)
        self.transactions_tab = TransactionsTab()
        self.user_mgmt_tab = UserManagementTab()
        self.product_mgmt_tab = ProductManagementTab()

        # Add tabs to widget
        self.tab_widget.addTab(self.overview_tab, "📊 Overview")
        self.tab_widget.addTab(self.transactions_tab, "💳 Transactions")
        self.tab_widget.addTab(self.user_mgmt_tab, "👥 User Management")
        self.tab_widget.addTab(self.product_mgmt_tab, "📦 Product Management")

        main_layout.addWidget(self.tab_widget)

    def _connect_tab_signals(self):
        """Connect signals from individual tabs to main signals"""
        # User Management tab signals
        self.user_mgmt_tab.add_user_signal.connect(self.add_user_signal.emit)
        self.user_mgmt_tab.delete_user_signal.connect(self.delete_user_signal.emit)
        self.user_mgmt_tab.search_users_signal.connect(self.search_users_signal.emit)

        # Product Management tab signals
        self.product_mgmt_tab.add_product_signal.connect(self.add_product_signal.emit)
        self.product_mgmt_tab.delete_product_signal.connect(self.delete_product_signal.emit)
        self.product_mgmt_tab.search_products_signal.connect(self.search_products_signal.emit)

        # Transactions tab signals (search only)
        self.transactions_tab.search_transactions_signal.connect(self.search_transactions_signal.emit)

    # ==================== UPDATE METHODS ====================
    def update_overview(self):
        """Update overview tab"""
        self.overview_tab.update_overview()

    def update_users_table(self, users, current_username=None):
        """Update users table — passes current_username down so the tab
        can disable the delete button on the logged-in user's row."""
        self.user_mgmt_tab.update_users_table(users, current_username)

    def update_products_table(self, products):
        """Update products table in product management tab"""
        self.product_mgmt_tab.update_products_table(products)

    def update_transactions_table(self, transactions):
        """Update transactions table in transactions tab"""
        self.transactions_tab.update_transactions_table(transactions)