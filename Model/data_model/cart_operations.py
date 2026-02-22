import logging
from Model.cart import CartItem
logger = logging.getLogger(__name__)

class CartOperations:
    def add_to_cart(self, product, quantity):
        # Check stock availability
        if not product.has_sufficient_stock(quantity):
            logger.warning(
                f"Insufficient stock for product '{product.name}' (requested: {quantity}, available: {product.stock})")
            return False

        # Check if product already in cart
        for item in self.cart:
            if item.product.product_id == product.product_id:
                # Update existing cart item
                if not product.has_sufficient_stock(quantity):
                    return False
                item.quantity = quantity
                logger.info(f"Updated cart: {product.name} quantity set to {quantity}")
                return True

        # Add new item to cart
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