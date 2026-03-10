import logging

logger = logging.getLogger(__name__)


class AuthController:
    def __init__(self, main_controller):
        self.main = main_controller
        self.model = main_controller.model
        self.main_window = main_controller.main_window
        self.stack = main_controller.stack
        self.current_user = None

    def handle_login(self, username, password):
        user = self.model.find_user_by_username(username)

        if user and user.verify_password(password):
            logger.info(f"User '{username}' authenticated successfully")
            self.current_user = user

            if user.is_admin():
                self.main.show_admin_dashboard()
            elif user.is_staff():
                self.main.show_pos_view()
            else:
                self.main.login_view.show_error(
                    "Error",
                    f"Unknown user role: {user.role}"
                )
                self.current_user = None
        else:
            logger.warning(f"Authentication failed for username '{username}'")
            self.main.login_view.show_error(
                "Login Failed",
                "Invalid username or password"
            )

    def handle_logout(self):
        confirmed = self.main.login_view.show_question(
            "Confirm Logout",
            "Are you sure you want to logout?"
        )

        if confirmed:
            self.current_user = None
            self.model.clear_cart()
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