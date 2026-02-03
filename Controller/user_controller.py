"""
User Management Controller
Handles user CRUD operations
"""
from PyQt6.QtWidgets import QMessageBox


class UserController:
    """Handles user management operations"""

    def __init__(self, main_controller):
        self.main = main_controller
        self.model = main_controller.model
        self.main_window = main_controller.main_window

    def handle_add_user(self, username, password, role):
        """Add a new user"""
        if self.model.add_user(username, password, role):
            QMessageBox.information(self.main_window, "Success", "User added successfully")
            self.main.admin_tabbed_view.update_users_table(
                self.model.users, self.model.current_user.username
            )
        else:
            QMessageBox.warning(self.main_window, "Error", "Username already exists")

    def handle_delete_user(self, username):
        """Delete a user with confirmation"""

        # ADDED: Block deleting yourself
        if self.model.current_user and username == self.model.current_user.username:
            QMessageBox.warning(
                self.main_window,
                "Cannot Delete",
                "You cannot delete your own account while you are logged in."
            )
            return

        reply = QMessageBox.question(
            self.main_window,
            "Confirm Delete",
            f"Are you sure you want to delete user '{username}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.model.delete_user(username)
            if success:
                QMessageBox.information(self.main_window, "Success", message)
                self.main.admin_tabbed_view.update_users_table(
                    self.model.users, self.model.current_user.username
                )
            else:
                QMessageBox.warning(self.main_window, "Error", message)

    def handle_search_users(self, search_term):
        """Search users by term"""
        filtered_users = self.model.search_users(search_term)
        self.main.admin_tabbed_view.update_users_table(
            filtered_users, self.model.current_user.username if self.model.current_user else None
        )