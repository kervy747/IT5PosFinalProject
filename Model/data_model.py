import logging
from Model.cart import CartItem

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataModel:

    def __init__(self):
        self.users = []
        self.products = []
        self.transactions = []
        self.cart = []

    #User Operations
    def find_user_by_username(self, username):
        return next((u for u in self.users if u.username == username), None)

    def authenticate(self, username, password):
        user = self.find_user_by_username(username)
        if user and user.verify_password(password):
            logger.info(f"User '{username}' authenticated successfully")
            return user
        logger.warning(f"Authentication failed for username '{username}'")
        return None

    def search_users(self, search_term):
        if not search_term:
            return self.users
        search_lower = search_term.lower()
        return [u for u in self.users if search_lower in u.username.lower()]

    #Product Operations
    def search_products(self, search_term):
        if not search_term:
            return self.products
        return [p for p in self.products if p.matches_search(search_term)]

    #Transaction Operations
    def search_transactions(self, search_term):
        if not search_term:
            return self.transactions
        return [t for t in self.transactions if t.matches_search(search_term)]

    #Cart Operations
    def add_to_cart(self, product, quantity):
        if not product.has_sufficient_stock(quantity):
            logger.warning(f"Insufficient stock for '{product.name}' (requested: {quantity}, available: {product.stock})")
            return False

        for item in self.cart:
            if item.product.product_id == product.product_id:
                new_quantity = item.quantity + quantity
                if not product.has_sufficient_stock(new_quantity):
                    logger.warning(f"Insufficient stock for '{product.name}' (cart + requested: {new_quantity}, available: {product.stock})")
                    return False
                item.quantity = new_quantity
                return True

        self.cart.append(CartItem(product, quantity))
        logger.info(f"Added to cart: {product.name} x {quantity}")
        return True

    def remove_from_cart(self, index):
        if 0 <= index < len(self.cart):
            removed_item = self.cart.pop(index)
            logger.info(f"Removed from cart: {removed_item.product.name}")

    def clear_cart(self):
        self.cart = []
        logger.info("Cart cleared")

    def get_cart_total(self):
        return sum(item.get_total() for item in self.cart)