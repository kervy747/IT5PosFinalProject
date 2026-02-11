import logging
from Model.user import User
from Controller.db import get_connection

logger = logging.getLogger(__name__)

class UserOperations:
    def load_users(self):
        try:
            conn = get_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT id, username, password, role, active FROM users")
            rows = cur.fetchall()

            self.users = []
            for row in rows:
                user = User(row['username'], row['password'], row['role'], row['active'])
                user.id = row['id']
                self.users.append(user)

            conn.close()
            logger.info(f"Loaded {len(self.users)} users from database")
        except Exception as e:
            logger.error(f"Error loading users: {e}")
            self.users = []

    def authenticate(self, username, password):
        user = self.find_user_by_username(username)

        if user and user.verify_password(password):
            logger.info(f"User '{username}' authenticated successfully")
            return user

        logger.warning(f"Authentication failed for username '{username}'")
        return None

    def find_user_by_username(self, username):
        return next((u for u in self.users if u.username == username), None)

    def add_user(self, username, password, role):
        # Check if username already exists
        if self.find_user_by_username(username):
            logger.warning(f"Cannot add user '{username}' - username already exists")
            return False

        try:
            # Create user with hashed password
            new_user = User.create_with_hashed_password(username, password, role)

            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                (new_user.username, new_user.password, new_user.role)
            )
            conn.commit()
            conn.close()

            self.load_users()  # Reload to get new user with ID
            logger.info(f"User '{username}' added successfully")
            return True
        except Exception as e:
            logger.error(f"Error adding user '{username}': {e}")
            return False

    def deactivate_user(self, username):
        """Deactivate a user account."""
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE users SET active = 0 WHERE username = %s", (username,))
            conn.commit()
            conn.close()

            self.load_users()
            logger.info(f"User '{username}' deactivated successfully")
            return True, "User deactivated successfully"
        except Exception as e:
            logger.error(f"Error deactivating user '{username}': {e}")
            return False, f"Error: {e}"

    def reactivate_user(self, username):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE users SET active = 1 WHERE username = %s", (username,))
            conn.commit()
            conn.close()

            self.load_users()
            logger.info(f"User '{username}' reactivated successfully")
            return True, "User reactivated successfully"
        except Exception as e:
            logger.error(f"Error reactivating user '{username}': {e}")
            return False, f"Error: {e}"

    def delete_user(self, username):
        # Check if deleting last admin
        admin_count = sum(1 for u in self.users if u.is_admin())
        user_to_delete = self.find_user_by_username(username)

        if user_to_delete and user_to_delete.is_admin() and admin_count <= 1:
            logger.warning(f"Cannot delete last admin user '{username}'")
            return False, "Cannot delete the last admin user"

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM users WHERE username = %s", (username,))
            conn.commit()
            conn.close()

            self.load_users()
            logger.info(f"User '{username}' deleted successfully")
            return True, "User deleted successfully"
        except Exception as e:
            logger.error(f"Error deleting user '{username}': {e}")
            return False, f"Error: {e}"

    def search_users(self, search_term):
        if not search_term:
            return self.users

        search_lower = search_term.lower()
        return [u for u in self.users if search_lower in u.username.lower()]

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