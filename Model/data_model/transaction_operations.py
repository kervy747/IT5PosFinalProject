import logging
logger = logging.getLogger(__name__)

class TransactionOperations:
    def search_transactions(self, search_term):
        if not search_term:
            return self.transactions

        search_lower = search_term.lower()
        return [t for t in self.transactions
                if search_lower in t.order_id.lower()
                or search_lower in t.staff_name.lower()]