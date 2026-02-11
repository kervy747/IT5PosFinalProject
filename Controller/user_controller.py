from PyQt6.QtWidgets import QMessageBox

class UserController:

    def __init__(self, main_controller):
        self.main = main_controller
        self.model = main_controller.model
        self.main_window = main_controller.main_window

    def handle_add_user(self, username, password, role):
        if self.model.add_user(username, password, role):
            QMessageBox.information(self.main_window, "Success", "User added successfully")
            current_username = self.main.auth.get_current_username()

            self.main.admin_tabbed_view.update_users_table(
                self.model.users,
                current_username
            )
        else:
            QMessageBox.warning(self.main_window, "Error", "Username already exists")

    def handle_delete_user(self, username):
        current_user = self.main.auth.get_current_user()

        # Prevent user from deactivating themselves
        if current_user and username == current_user.username:
            QMessageBox.warning(
                self.main_window,
                "Cannot Deactivate",
                "You cannot deactivate your own account while you are logged in."
            )
            return

        # Confirm deactivation
        reply = QMessageBox.question(
            self.main_window,
            "Confirm Deactivate",
            f"Are you sure you want to deactivate user '{username}'?\n\n"
            "They will no longer be able to login, but their transaction history will be preserved.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.model.deactivate_user(username)
            if success:
                QMessageBox.information(self.main_window, "Success", message)

                current_username = self.main.auth.get_current_username()

                self.main.admin_tabbed_view.update_users_table(
                    self.model.users,
                    current_username
                )
            else:
                QMessageBox.warning(self.main_window, "Error", message)

    def handle_reactivate_user(self, username):
        reply = QMessageBox.question(
            self.main_window,
            "Confirm Reactivate",
            f"Are you sure you want to reactivate user '{username}'?\n\n"
            "They will be able to login again.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.model.reactivate_user(username)
            if success:
                QMessageBox.information(self.main_window, "Success", message)

                current_username = self.main.auth.get_current_username()

                self.main.admin_tabbed_view.update_users_table(
                    self.model.users,
                    current_username
                )
            else:
                QMessageBox.warning(self.main_window, "Error", message)

    def handle_search_users(self, search_term):
        filtered_users = self.model.search_users(search_term)

        current_username = self.main.auth.get_current_username()

        self.main.admin_tabbed_view.update_users_table(
            filtered_users,
            current_username
        )