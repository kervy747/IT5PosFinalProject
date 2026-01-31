from datetime import datetime


class Transaction:
    def __init__(self, order_id, staff_name, items, total_amount, date):
        self.order_id = order_id
        self.staff_name = staff_name
        self.items = items
        self.total_amount = total_amount
        self.date = date
        self.user_id = None  # NEW: Will be set after loading from database

    def to_dict(self):
        return {
            'order_id': self.order_id,
            'staff_name': self.staff_name,
            'user_id': self.user_id,  # NEW: Include user_id in dict
            'items': self.items,
            'total_amount': self.total_amount,
            'date': self.date
        }

    @staticmethod
    def from_dict(data):
        transaction = Transaction(
            data['order_id'],
            data['staff_name'],
            data['items'],
            data['total_amount'],
            data['date']
        )
        transaction.user_id = data.get('user_id')  # NEW: Load user_id if present
        return transaction

    def get_total_items(self):
        return sum(item['quantity'] for item in self.items)

    def get_item_ids(self):
        return [item['product_id'] for item in self.items]

    def __repr__(self):
        return f"Transaction({self.order_id}, User ID: {self.user_id}, Staff: {self.staff_name}, Total: ₱{self.total_amount:.2f})"