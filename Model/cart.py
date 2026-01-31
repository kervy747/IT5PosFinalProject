class CartItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def get_total(self):
        return self.product.price * self.quantity

    def __repr__(self):
        return f"CartItem({self.product.product_id}, {self.product.name}, Qty: {self.quantity}, Total: ₱{self.get_total():.2f})"