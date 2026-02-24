import logging

logger = logging.getLogger(__name__)

class UserOperations:

    def authenticate(self, username, password):
        user = self.find_user_by_username(username)

        if user and user.verify_password(password):
            logger.info(f"User '{username}' authenticated successfully")
            return user

        logger.warning(f"Authentication failed for username '{username}'")
        return None

    def find_user_by_username(self, username):
        return next((u for u in self.users if u.username == username), None)

    def search_users(self, search_term):
        if not search_term:
            return self.users

        search_lower = search_term.lower()
        return [u for u in self.users if search_lower in u.username.lower()]