"""
Authentication Controller
Handles login, logout, and role-based navigation
"""
from PyQt6.QtWidgets import QMessageBox


class AuthController:

    def __init__(self, main_controller):
        self.main = main_controller
        self.model = main_controller.model
        self.main_window = main_controller.main_window
        self.stack = main_controller.stack
        self.current_user = None

    def handle_login(self, username, password):
        """Handle login attempt"""
        if self.model.authenticate(username, password):
            self.current_user = self.model.current_user
            user_role = self.current_user.role

            if user_role == "admin":
                # Admin goes to tabbed dashboard with overview shown first
                self.main.show_admin_dashboard()
            elif user_role == "staff":
                # Staff goes directly to POS
                self.main.pos_view.update_products(self.model.products)
                self.main.pos_view.update_cart(self.model.cart, self.model.get_cart_total())
                self.stack.setCurrentWidget(self.main.pos_view)
            else:
                QMessageBox.warning(self.main_window, "Error", "Unknown user role")
        else:
            QMessageBox.warning(
                self.main_window,
                "Login Failed",
                "Invalid username or password"
            )

    def handle_logout(self):
        """Handle logout"""
        reply = QMessageBox.question(
            self.main_window,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.current_user = None
            self.model.current_user = None
            self.model.clear_cart()
            self.stack.setCurrentWidget(self.main.login_view)
            self.main.login_view.username_input.clear()
            self.main.login_view.password_input.clear()