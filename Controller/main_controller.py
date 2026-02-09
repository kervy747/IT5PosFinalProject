from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from PyQt6.QtGui import QPalette, QColor
from View.colors import *
from View.adminTabbedView import AdminTabbedView

from .auth_controller import AuthController
from .user_controller import UserController
from .product_controller import ProductController
from .pos_controller import POSOperationsController
from .transaction_controller import TransactionController


class POSController:
    """
    Main controller that coordinates all sub-controllers.

    Responsibilities:
    - Initialize and manage the main window
    - Coordinate between sub-controllers
    - Handle view navigation/switching
    - Connect view signals to appropriate controller handlers

    Does NOT:
    - Contain business logic (delegated to sub-controllers)
    - Directly manipulate data (delegated to Model)
    - Show UI dialogs (delegated to Views)
    """

    def __init__(self, model, login_view, pos_view):
        self.model = model

        # Initialize main window
        self.main_window = QMainWindow()
        self.main_window.setWindowTitle("POS System")
        self.main_window.setGeometry(100, 100, 1200, 700)

        # Set color scheme
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(BACKGROUND))
        self.main_window.setPalette(palette)

        # Store views
        self.login_view = login_view
        self.pos_view = pos_view
        self.admin_tabbed_view = AdminTabbedView(self.model)

        # Setup stack widget with all views
        self.stack = QStackedWidget()
        self.stack.addWidget(self.login_view)
        self.stack.addWidget(self.admin_tabbed_view)
        self.stack.addWidget(self.pos_view)
        self.main_window.setCentralWidget(self.stack)

        # Initialize sub-controllers
        self.auth = AuthController(self)
        self.user = UserController(self)
        self.product = ProductController(self)
        self.pos_ops = POSOperationsController(self)
        self.transaction = TransactionController(self)

        # Connect all signals
        self._connect_signals()

    def _connect_signals(self):
        """Connect view signals to controller handlers"""

        # Authentication signals
        self.login_view.login_signal.connect(self.auth.handle_login)
        self.admin_tabbed_view.logout_signal.connect(self.auth.handle_logout)
        self.pos_view.logout_signal.connect(self.auth.handle_logout)

        # User management signals
        self.admin_tabbed_view.add_user_signal.connect(self.user.handle_add_user)
        self.admin_tabbed_view.delete_user_signal.connect(self.user.handle_delete_user)
        self.admin_tabbed_view.reactivate_user_signal.connect(self.user.handle_reactivate_user)
        self.admin_tabbed_view.search_users_signal.connect(self.user.handle_search_users)

        # Product management signals
        self.admin_tabbed_view.add_product_signal.connect(self.product.handle_add_product)
        self.admin_tabbed_view.delete_product_signal.connect(self.product.handle_delete_product)
        self.admin_tabbed_view.search_products_signal.connect(self.product.handle_search_products)

        # Transaction management signals
        self.admin_tabbed_view.search_transactions_signal.connect(self.transaction.handle_search_transactions)
        # Add this if you have delete transaction functionality in your view:
        # self.admin_tabbed_view.delete_transaction_signal.connect(self.transaction.handle_delete_transaction)

        # POS operation signals
        self.pos_view.add_to_cart_signal.connect(self.pos_ops.handle_add_to_cart)
        self.pos_view.remove_from_cart_signal.connect(self.pos_ops.handle_remove_from_cart)
        self.pos_view.complete_sale_signal.connect(self.pos_ops.handle_complete_sale)

    def show_admin_dashboard(self):
        """
        Navigate to admin dashboard and refresh all data.
        Called after successful admin login or when returning to dashboard.
        """
        # Update all dashboard views with current data
        self.admin_tabbed_view.update_overview()

        # Get current username for display (None-safe)
        current_username = self.model.current_user.username if self.model.current_user else None

        self.admin_tabbed_view.update_users_table(
            self.model.users,
            current_username
        )
        self.admin_tabbed_view.update_products_table(self.model.products)
        self.admin_tabbed_view.update_transactions_table(self.model.transactions)

        # Show overview tab by default
        self.admin_tabbed_view.tab_widget.setCurrentIndex(0)

        # Switch to admin dashboard view
        self.stack.setCurrentWidget(self.admin_tabbed_view)

    def show_pos_view(self):
        """
        Navigate to POS view and refresh data.
        Called after successful staff login or when returning to POS.
        """
        self.pos_view.update_products(self.model.products)
        self.pos_view.update_cart(self.model.cart, self.model.get_cart_total())
        self.stack.setCurrentWidget(self.pos_view)

    def show_login_view(self):
        """
        Navigate to login view.
        Called after logout or on application start.
        """
        self.login_view.clear_fields()
        self.stack.setCurrentWidget(self.login_view)

    def run(self):
        """Start the application"""
        self.main_window.show()