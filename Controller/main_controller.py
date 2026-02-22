from .auth_controller import AuthController
from .user_controller import UserController
from .product_controller import ProductController
from .pos_controller import POSOperationsController
from .transaction_controller import TransactionController

class POSController:
    def __init__(self, model, login_view, pos_view, admin_tabbed_view, main_window, stack):
        self.model = model
        self.main_window = main_window
        self.stack = stack
        self.login_view = login_view
        self.pos_view = pos_view
        self.admin_tabbed_view = admin_tabbed_view

        self.stack.addWidget(self.login_view)
        self.stack.addWidget(self.admin_tabbed_view)
        self.stack.addWidget(self.pos_view)

        self.auth = AuthController(self)
        self.user = UserController(self)
        self.product = ProductController(self)
        self.pos_ops = POSOperationsController(self)
        self.transaction = TransactionController(self)

        self._connect_signals()

    def _connect_signals(self):
        self.login_view.login_signal.connect(self.auth.handle_login)
        self.admin_tabbed_view.logout_signal.connect(self.auth.handle_logout)
        self.pos_view.logout_signal.connect(self.auth.handle_logout)

        self.admin_tabbed_view.add_user_signal.connect(self.user.handle_add_user)
        self.admin_tabbed_view.delete_user_signal.connect(self.user.handle_delete_user)
        self.admin_tabbed_view.reactivate_user_signal.connect(self.user.handle_reactivate_user)
        self.admin_tabbed_view.search_users_signal.connect(self.user.handle_search_users)

        self.admin_tabbed_view.add_product_signal.connect(self.product.handle_add_product)
        self.admin_tabbed_view.delete_product_signal.connect(self.product.handle_delete_product)
        self.admin_tabbed_view.search_products_signal.connect(self.product.handle_search_products)

        self.admin_tabbed_view.search_transactions_signal.connect(self.transaction.handle_search_transactions)
        self.admin_tabbed_view.filter_by_month_signal.connect(self.transaction.handle_filter_by_month)

        self.pos_view.add_to_cart_signal.connect(self.pos_ops.handle_add_to_cart)
        self.pos_view.remove_from_cart_signal.connect(self.pos_ops.handle_remove_from_cart)
        self.pos_view.complete_sale_signal.connect(self.pos_ops.handle_complete_sale)

    def show_admin_dashboard(self):
        self.admin_tabbed_view.update_overview()

        current_username = self.auth.get_current_username()

        self.admin_tabbed_view.update_users_table(
            self.model.users,
            current_username
        )
        self.admin_tabbed_view.update_products_table(self.model.products)
        self.admin_tabbed_view.update_transactions_table(self.model.transactions)

        self.admin_tabbed_view.tab_widget.setCurrentIndex(0)

        self.stack.setCurrentWidget(self.admin_tabbed_view)

    def show_pos_view(self):
        self.pos_view.update_products(self.model.products)
        self.pos_view.update_cart(self.model.cart, self.model.get_cart_total())
        self.stack.setCurrentWidget(self.pos_view)

    def show_login_view(self):
        self.login_view.clear_fields()
        self.stack.setCurrentWidget(self.login_view)

    def run(self):
        self.main_window.show()