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

    # User Operations
    def find_user_by_username(self, username):
        return next((u for u in self.users if u.username == username), None)

    # Product Operations
    def get_all_products(self):
        return self.products

    # Cart Operations
    def get_cart_item_by_product_id(self, product_id):
        return next((item for item in self.cart if item.product.product_id == product_id), None)

    def append_cart_item(self, product, quantity):
        self.cart.append(CartItem(product, quantity))
        logger.info(f"Added to cart: {product.name} x {quantity}")

    def update_cart_item_quantity(self, product_id, additional_quantity):
        existing = self.get_cart_item_by_product_id(product_id)
        existing.quantity += additional_quantity
        logger.info(f"Updated cart item quantity for product {product_id} by +{additional_quantity}")

    def remove_from_cart(self, index):
        removed_item = self.cart.pop(index)
        logger.info(f"Removed from cart: {removed_item.product.name}")

    def clear_cart(self):
        self.cart = []
        logger.info("Cart cleared")

    def get_cart_total(self):
        return sum(item.get_total() for item in self.cart)