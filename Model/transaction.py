from datetime import datetime

class Transaction:
    def __init__(self, order_id, staff_name, items, total_amount, date):
        self.order_id = order_id
        self.staff_name = staff_name
        self.items = items
        self.total_amount = total_amount
        self.date = date

    def to_dict(self):
        return {
            'order_id': self.order_id,
            'staff_name': self.staff_name,
            'items': self.items,
            'total_amount': self.total_amount,
            'date': self.date
        }

    @staticmethod
    def from_dict(data):
        return Transaction(
            data['order_id'],
            data['staff_name'],
            data['items'],
            data['total_amount'],
            data['date']
        )

    def get_total_items(self):
        return sum(item['quantity'] for item in self.items)

    def get_item_ids(self):
        return [item['product_id'] for item in self.items]