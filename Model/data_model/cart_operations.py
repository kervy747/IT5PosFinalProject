import logging
from Model.cart import CartItem
logger = logging.getLogger(__name__)

class CartOperations:
    def add_to_cart(self, product, quantity):
        if not product.has_sufficient_stock(quantity):
            logger.warning(
                f"Insufficient stock for product '{product.name}' (requested: {quantity}, available: {product.stock})")
            return False

        for item in self.cart:
            if item.product.product_id == product.product_id:
                new_quantity = item.quantity + quantity
                if not product.has_sufficient_stock(new_quantity):
                    logger.warning(
                        f"Insufficient stock for product '{product.name}' (cart + requested: {new_quantity}, available: {product.stock})")
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