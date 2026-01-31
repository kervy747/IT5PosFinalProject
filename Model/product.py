class Product:
    def __init__(self, product_id, name, price, stock):
        # NEW: Now uses product_id (VARCHAR: PR#####) instead of id (INT)
        self.product_id = product_id
        self.name = name
        self.price = float(price)
        self.stock = int(stock)

    @property
    def id(self):
        """Backward compatibility - returns product_id"""
        return self.product_id

    def to_dict(self):
        return {
            'product_id': self.product_id,  # NEW: Changed from 'id' to 'product_id'
            'id': self.product_id,  # Keep 'id' for backward compatibility
            'name': self.name,
            'price': self.price,
            'stock': self.stock
        }

    @staticmethod
    def from_dict(data):
        # Support both 'product_id' and 'id' keys for backward compatibility
        product_id = data.get('product_id') or data.get('id')
        return Product(product_id, data['name'], data['price'], data['stock'])

    def __repr__(self):
        return f"Product({self.product_id}, {self.name}, ₱{self.price:.2f}, Stock: {self.stock})"