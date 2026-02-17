import logging
from datetime import datetime
from Model.transaction import Transaction
from Controller.db import get_connection
logger = logging.getLogger(__name__)


class TransactionOperations:
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

            self.transactions = []
            for trans in transaction_rows:
                # Load transaction items
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
                self.transactions.append(transaction)

            conn.close()
            logger.info(f"Loaded {len(self.transactions)} transactions from database")
        except Exception as e:
            logger.error(f"Error loading transactions: {e}")
            self.transactions = []

    def complete_sale(self, current_user):
        if not self._validate_sale(current_user):
            return False

        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()

            # Generate order ID
            order_id = self._generate_next_order_id(cur)

            # Prepare cart items
            items = self._prepare_cart_items()

            # Get user ID
            user_id = self._get_user_id(cur, current_user)

            # Insert transaction
            transaction_id = self._insert_transaction(cur, order_id, user_id, current_user.username, items)

            # Insert transaction items and update stock
            self._insert_transaction_items(cur, transaction_id, items)
            self._update_product_stock(cur, items)

            conn.commit()
            logger.info(f"Sale completed successfully: {order_id}")

            # Finalize sale
            self._finalize_sale()

            return True

        except Exception as e:
            logger.error(f"Error completing sale: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()

    def _validate_sale(self, current_user):
        if not self.cart:
            logger.warning("Cannot complete sale: Cart is empty")
            return False

        if not current_user:
            logger.warning("Cannot complete sale: No current user")
            return False

        return True

    def _prepare_cart_items(self):
        return [{
            'product_id': item.product.product_id,
            'product_name': item.product.name,
            'quantity': item.quantity,
            'price': item.product.price
        } for item in self.cart]

    def _get_user_id(self, cursor, current_user):
        cursor.execute("SELECT id FROM users WHERE username = %s", (current_user.username,))
        result = cursor.fetchone()

        if not result:
            raise ValueError(f"User '{current_user.username}' not found in database")

        return result[0]

    def _insert_transaction(self, cursor, order_id, user_id, staff_name, items):
        cursor.execute(
            "INSERT INTO transactions (order_id, user_id, staff_name, total_amount, date) "
            "VALUES (%s, %s, %s, %s, %s)",
            (
                order_id,
                user_id,
                staff_name,
                self.get_cart_total(),
                datetime.now().strftime("%m-%d-%Y %I:%M %p")
            )
        )
        return cursor.lastrowid

    def _insert_transaction_items(self, cursor, transaction_id, items):
        for item in items:
            cursor.execute(
                "INSERT INTO transaction_items (transaction_id, product_id, product_name, quantity, price) "
                "VALUES (%s, %s, %s, %s, %s)",
                (
                    transaction_id,
                    item['product_id'],
                    item['product_name'],
                    item['quantity'],
                    item['price']
                )
            )

    def _update_product_stock(self, cursor, items):
        for item in items:
            cursor.execute(
                "UPDATE products SET stock = stock - %s WHERE product_id = %s",
                (item["quantity"], item["product_id"])
            )

    def _finalize_sale(self):
        self.clear_cart()
        self.load_products()
        self.load_transactions()

    def delete_transaction(self, order_id):
        try:
            conn = get_connection()
            cur = conn.cursor()

            # Get transaction ID
            cur.execute("SELECT id FROM transactions WHERE order_id = %s", (order_id,))
            result = cur.fetchone()

            if not result:
                conn.close()
                logger.warning(f"Transaction '{order_id}' not found")
                return False, "Transaction not found"

            transaction_id = result[0]

            # Delete transaction items first (foreign key constraint)
            cur.execute("DELETE FROM transaction_items WHERE transaction_id = %s", (transaction_id,))

            # Delete the transaction
            cur.execute("DELETE FROM transactions WHERE id = %s", (transaction_id,))

            conn.commit()
            conn.close()

            self.load_transactions()
            logger.info(f"Transaction '{order_id}' deleted successfully")
            return True, "Transaction deleted successfully"
        except Exception as e:
            logger.error(f"Error deleting transaction '{order_id}': {e}")
            return False, f"Error: {e}"

    def search_transactions(self, search_term):
        if not search_term:
            return self.transactions

        search_lower = search_term.lower()
        return [t for t in self.transactions
                if search_lower in t.order_id.lower()
                or search_lower in t.staff_name.lower()]