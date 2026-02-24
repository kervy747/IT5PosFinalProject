import logging
from datetime import datetime
from Controller.db import get_connection
from Model.transaction import Transaction

logger = logging.getLogger(__name__)


class TransactionController:
    def __init__(self, main_controller):
        self.main = main_controller
        self.model = main_controller.model
        self.main_window = main_controller.main_window

    def load_transactions(self):
        try:
            conn = get_connection()
            cur = conn.cursor(dictionary=True)

            cur.execute("""
                SELECT id, order_id, user_id, staff_name, total_amount, date
                FROM transactions
                ORDER BY id DESC
            """)
            transaction_rows = cur.fetchall()

            self.model.transactions = []
            for trans in transaction_rows:
                cur.execute("""
                    SELECT product_id, product_name, quantity, price
                    FROM transaction_items
                    WHERE transaction_id = %s
                """, (trans['id'],))

                items = []
                for item_row in cur.fetchall():
                    items.append({
                        'product_id': item_row['product_id'],
                        'product_name': item_row['product_name'],
                        'quantity': item_row['quantity'],
                        'price': float(item_row['price'])
                    })

                transaction = Transaction(
                    trans["order_id"],
                    trans["staff_name"],
                    items,
                    float(trans["total_amount"]),
                    trans["date"]
                )
                transaction.user_id = trans["user_id"]
                self.model.transactions.append(transaction)

            conn.close()
            logger.info(f"Loaded {len(self.model.transactions)} transactions from database")
        except Exception as e:
            logger.error(f"Error loading transactions: {e}")
            self.model.transactions = []

    def _generate_next_order_id(self, cursor):
        cursor.execute("SELECT setting_value FROM system_settings WHERE setting_key = 'next_order_number'")
        result = cursor.fetchone()

        if result:
            next_number = int(result[0])
        else:
            next_number = 1
            cursor.execute(
                "INSERT INTO system_settings (setting_key, setting_value) VALUES ('next_order_number', '1')"
            )

        order_id = f"OR{next_number:04d}"

        cursor.execute(
            "UPDATE system_settings SET setting_value = %s WHERE setting_key = 'next_order_number'",
            (next_number + 1,)
        )

        return order_id

    def _filter_by_month(self, transactions, month, year):
        filtered = []
        for t in transactions:
            try:
                trans_date = datetime.strptime(t.date, "%m-%d-%Y %I:%M %p")
                if trans_date.month == month and trans_date.year == year:
                    filtered.append(t)
            except Exception:
                pass
        return filtered

    def handle_search_transactions(self, search_term):
        filtered_transactions = self.model.search_transactions(search_term)
        self.main.admin_tabbed_view.update_transactions_table(filtered_transactions)

    def handle_filter_by_month(self, month, year):
        filtered = self._filter_by_month(self.model.transactions, month, year)
        self.main.admin_tabbed_view.update_transactions_table(filtered)

    def handle_delete_transaction(self, order_id):
        confirmed = self.main.admin_tabbed_view.transactions_tab.show_question(
            "Confirm Delete",
            f"Are you sure you want to delete transaction '{order_id}'?\n\n"
            "This action cannot be undone."
        )

        if confirmed:
            try:
                conn = get_connection()
                cur = conn.cursor()

                cur.execute("SELECT id FROM transactions WHERE order_id = %s", (order_id,))
                result = cur.fetchone()

                if not result:
                    conn.close()
                    logger.warning(f"Transaction '{order_id}' not found")
                    self.main.admin_tabbed_view.transactions_tab.show_error("Error", "Transaction not found")
                    return

                transaction_id = result[0]

                cur.execute("DELETE FROM transaction_items WHERE transaction_id = %s", (transaction_id,))
                cur.execute("DELETE FROM transactions WHERE id = %s", (transaction_id,))

                conn.commit()
                conn.close()

                self.load_transactions()
                logger.info(f"Transaction '{order_id}' deleted successfully")

                now = datetime.now()
                filtered = self._filter_by_month(self.model.transactions, now.month, now.year)
                self.main.admin_tabbed_view.transactions_tab.show_info("Success", "Transaction deleted successfully")
                self.main.admin_tabbed_view.update_transactions_table(filtered)
                if hasattr(self.main, 'overview_view'):
                    self.main.overview_view.update_overview(self.model.transactions, self.model.products)
            except Exception as e:
                logger.error(f"Error deleting transaction '{order_id}': {e}")
                self.main.admin_tabbed_view.transactions_tab.show_error("Error", f"Error: {e}")