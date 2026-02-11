class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.price = float(price)
        self.stock = int(stock)

    def has_sufficient_stock(self, quantity):
        return self.stock >= quantity

    def is_available(self):
        return self.stock > 0

    def reduce_stock(self, quantity):
        if not self.has_sufficient_stock(quantity):
            return False
        self.stock -= quantity
        return True

    def increase_stock(self, quantity):self.stock += quantity

    def set_stock(self, new_stock):
        self.stock = max(0, int(new_stock))  # Ensure non-negative

    def get_value(self):
        return self.price * self.stock


    @property
    def id(self):
        return self.product_id

    def to_dict(self):
        return {
            'product_id': self.product_id,
            'id': self.product_id,
            'name': self.name,
            'price': self.price,
            'stock': self.stock
        }

    @staticmethod
    def from_dict(data):
        product_id = data.get('product_id') or data.get('id')
        return Product(product_id, data['name'], data['price'], data['stock'])

    def __repr__(self):
        availability = "In Stock" if self.is_available() else "Out of Stock"
        return f"Product({self.product_id}, {self.name}, ₱{self.price:.2f}, Stock: {self.stock} - {availability})"