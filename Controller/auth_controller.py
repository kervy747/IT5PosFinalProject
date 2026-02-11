from PyQt6.QtWidgets import QMessageBox


class AuthController:
    def __init__(self, main_controller):
        self.main = main_controller
        self.model = main_controller.model
        self.main_window = main_controller.main_window
        self.stack = main_controller.stack
        self.current_user = None

    def handle_login(self, username, password):
        authenticated_user = self.model.authenticate(username, password)

        if authenticated_user:
            self.current_user = authenticated_user

            # Route based on role
            if authenticated_user.is_admin():
                # Admin goes to dashboard
                self.main.show_admin_dashboard()
            elif authenticated_user.is_staff():
                # Staff goes to POS
                self.main.show_pos_view()
            else:
                # Unknown role - show error
                self.main.login_view.show_error(
                    "Error",
                    f"Unknown user role: {authenticated_user.role}"
                )
                self.current_user = None  # Clear invalid user
        else:
            self.main.login_view.show_error(
                "Login Failed",
                "Invalid username or password"
            )

    def handle_logout(self):
        current_view = self.stack.currentWidget()

        reply = QMessageBox.question(
            self.main_window,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Clear user session
            self.current_user = None

            # Clear cart
            self.model.clear_cart()

            # Return to login screen
            self.main.show_login_view()

    # ==================== Convenience Methods ====================

    def get_current_user(self):
        return self.current_user

    def get_current_username(self):
        return self.current_user.username if self.current_user else None

    def get_current_user_role(self):
        return self.current_user.role if self.current_user else None

    def is_authenticated(self):
        return self.current_user is not None

    def is_current_user_admin(self):
        return self.current_user is not None and self.current_user.is_admin()

    def is_current_user_staff(self):
        return self.current_user is not None and self.current_user.is_staff()