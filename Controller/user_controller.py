import logging
from Controller.db import get_connection
from Model.user import User
logger = logging.getLogger(__name__)

class UserController:
    def __init__(self, main_controller):
        self.main = main_controller
        self.model = main_controller.model
        self.main_window = main_controller.main_window

    def load_users(self):
        try:
            conn = get_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT id, username, password, role, active FROM users")
            rows = cur.fetchall()

            self.model.users = []
            for row in rows:
                user = User(row['username'], row['password'], row['role'], row['active'])
                user.id = row['id']
                self.model.users.append(user)

            conn.close()
            logger.info(f"Loaded {len(self.model.users)} users from database")
        except Exception as e:
            logger.error(f"Error loading users: {e}")
            self.model.users = []

    def handle_add_user(self, username, password, role):
        if self.model.find_user_by_username(username):
            self.main.admin_tabbed_view.user_mgmt_tab.show_error("Error", "Username already exists")
            return

        try:
            new_user = User.create_with_hashed_password(username, password, role)

            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                (new_user.username, new_user.password, new_user.role)
            )
            conn.commit()
            conn.close()

            self.load_users()
            logger.info(f"User '{username}' added successfully")

            self.main.admin_tabbed_view.user_mgmt_tab.show_info("Success", "User added successfully")
            current_username = self.main.auth.get_current_username()
            self.main.admin_tabbed_view.update_users_table(self.model.users, current_username)
        except Exception as e:
            logger.error(f"Error adding user '{username}': {e}")
            self.main.admin_tabbed_view.user_mgmt_tab.show_error("Error", f"Failed to add user: {e}")

    def handle_delete_user(self, username):
        current_user = self.main.auth.get_current_user()

        if current_user and username == current_user.username:
            self.main.admin_tabbed_view.user_mgmt_tab.show_error(
                "Cannot Deactivate",
                "You cannot deactivate your own account while you are logged in."
            )
            return

        confirmed = self.main.admin_tabbed_view.user_mgmt_tab.show_question(
            "Confirm Deactivate",
            f"Are you sure you want to deactivate user '{username}'?\n\n"
            "They will no longer be able to login, but their transaction history will be preserved."
        )

        if confirmed:
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("UPDATE users SET active = 0 WHERE username = %s", (username,))
                conn.commit()
                conn.close()

                self.load_users()
                logger.info(f"User '{username}' deactivated successfully")

                self.main.admin_tabbed_view.user_mgmt_tab.show_info("Success", "User deactivated successfully")
                current_username = self.main.auth.get_current_username()
                self.main.admin_tabbed_view.update_users_table(self.model.users, current_username)
            except Exception as e:
                logger.error(f"Error deactivating user '{username}': {e}")
                self.main.admin_tabbed_view.user_mgmt_tab.show_error("Error", f"Error: {e}")

    def handle_reactivate_user(self, username):
        confirmed = self.main.admin_tabbed_view.user_mgmt_tab.show_question(
            "Confirm Reactivate",
            f"Are you sure you want to reactivate user '{username}'?\n\n"
            "They will be able to login again."
        )

        if confirmed:
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("UPDATE users SET active = 1 WHERE username = %s", (username,))
                conn.commit()
                conn.close()

                self.load_users()
                logger.info(f"User '{username}' reactivated successfully")

                self.main.admin_tabbed_view.user_mgmt_tab.show_info("Success", "User reactivated successfully")
                current_username = self.main.auth.get_current_username()
                self.main.admin_tabbed_view.update_users_table(self.model.users, current_username)
            except Exception as e:
                logger.error(f"Error reactivating user '{username}': {e}")
                self.main.admin_tabbed_view.user_mgmt_tab.show_error("Error", f"Error: {e}")

    def handle_search_users(self, search_term):
        filtered_users = self.model.search_users(search_term)
        current_username = self.main.auth.get_current_username()
        self.main.admin_tabbed_view.update_users_table(filtered_users, current_username)

    def get_user_by_id(self, user_id):
        try:
            conn = get_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT id, username, role FROM users WHERE id = %s", (user_id,))
            result = cur.fetchone()
            conn.close()
            return result
        except Exception as e:
            logger.error(f"Error getting user by ID {user_id}: {e}")
            return None