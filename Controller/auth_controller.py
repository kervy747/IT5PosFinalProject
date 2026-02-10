from PyQt6.QtWidgets import QMessageBox


class AuthController:
    def __init__(self, main_controller):
        self.main = main_controller
        self.model = main_controller.model
        self.main_window = main_controller.main_window
        self.stack = main_controller.stack
        self.current_user = None

    def handle_login(self, username, password):
        # Authenticate with model
        if self.model.authenticate(username, password):
            self.current_user = self.model.current_user
            user_role = self.current_user.role

            # Route based on role
            if user_role == "admin":
                # Admin goes to dashboard
                self.main.show_admin_dashboard()
            elif user_role == "staff":
                # Staff goes to POS
                self.main.show_pos_view()
            else:
                # Unknown role - show error via View
                self.main.login_view.show_error(
                    "Error",
                    "Unknown user role"
                )
        else:
            # Authentication failed - show error via View
            self.main.login_view.show_error(
                "Login Failed",
                "Invalid username or password"
            )

    def handle_logout(self):
        current_view = self.stack.currentWidget()

        # Show confirmation dialog
        reply = QMessageBox.question(
            self.main_window,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Clear user session
            self.current_user = None
            self.model.current_user = None
            self.model.clear_cart()

            # Return to login screen
            self.main.show_login_view()

    def get_current_username(self):
        return self.current_user.username if self.current_user else None

    def get_current_user_role(self):
        return self.current_user.role if self.current_user else None

    def is_authenticated(self):
        return self.current_user is not None