import sys
import os
from datetime import datetime
from .user import User
from .product import Product
from .cart import CartItem
from .transaction import Transaction

# Import from Controller folder (sibling directory)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Controller.db import get_connection


class DataModel:
    def __init__(self):
        self.users = []
        self.products = []
        self.transactions = []
        self.cart = []
        self.current_user = None

        self.load_users()
        self.load_products()
        self.load_transactions()

    def load_users(self):
        """Load users from MySQL database"""
        try:
            print("Connecting to database for users...")
            conn = get_connection()
            print("Connected! Fetching users...")
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT username, password, role FROM users")
            rows = cur.fetchall()
            self.users = [User(row['username'], row['password'], row['role']) for row in rows]
            conn.close()
            print(f"Loaded {len(self.users)} users successfully")
        except Exception as e:
            print(f"ERROR loading users: {e}")
            import traceback
            traceback.print_exc()
            self.users = []

    def load_products(self):
        """Load products from MySQL database"""
        try:
            print("Connecting to database for products...")
            conn = get_connection()
            print("Connected! Fetching products...")
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT id, name, price, stock FROM products")
            rows = cur.fetchall()
            self.products = [Product(row['id'], row['name'], row['price'], row['stock']) for row in rows]
            conn.close()
            print(f"Loaded {len(self.products)} products successfully")
        except Exception as e:
            print(f"ERROR loading products: {e}")
            import traceback
            traceback.print_exc()
            self.products = []

    def load_transactions(self):
        """Load transactions from MySQL database (with separate transaction_items table)"""
        try:
            print("Connecting to database for transactions...")
            conn = get_connection()
            print("Connected! Fetching transactions...")
            cur = conn.cursor(dictionary=True)

            # Get all transactions
            cur.execute("""
                SELECT id, order_id, staff_name, total_amount, date
                FROM transactions
                ORDER BY id DESC
            """)
            transaction_rows = cur.fetchall()

            self.transactions = []
            for trans in transaction_rows:
                # Get items for this transaction
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

                # Create Transaction object
                self.transactions.append(Transaction(
                    trans["order_id"],
                    trans["staff_name"],
                    items,
                    float(trans["total_amount"]),
                    trans["date"]
                ))

            conn.close()
            print(f"Loaded {len(self.transactions)} transactions successfully")
        except Exception as e:
            print(f"ERROR loading transactions: {e}")
            import traceback
            traceback.print_exc()
            self.transactions = []

    def delete_transaction(self, order_id):
        """Delete a transaction by order ID from MySQL database"""
        try:
            conn = get_connection()
            cur = conn.cursor()

            # First, get the transaction_id for this order_id
            cur.execute("SELECT id FROM transactions WHERE order_id = %s", (order_id,))
            result = cur.fetchone()

            if not result:
                conn.close()
                return False, "Transaction not found"

            transaction_id = result[0]

            # Delete transaction items first (foreign key constraint)
            cur.execute("DELETE FROM transaction_items WHERE transaction_id = %s", (transaction_id,))

            # Delete the transaction
            cur.execute("DELETE FROM transactions WHERE id = %s", (transaction_id,))

            conn.commit()
            conn.close()

            # Reload transactions from database
            self.load_transactions()

            return True, "Transaction deleted successfully"
        except Exception as e:
            print(f"Error deleting transaction: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Error: {e}"

    def authenticate(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                self.current_user = user
                return True
        return False

    def add_user(self, username, password, role):
        """Add user to MySQL database"""
        if any(u.username == username for u in self.users):
            return False

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                (username, password, role)
            )
            conn.commit()
            conn.close()
            self.load_users()
            return True
        except Exception as e:
            print(f"Error adding user: {e}")
            return False

    def delete_user(self, username):
        """Delete a user by username"""
        admin_count = sum(1 for u in self.users if u.role == 'admin')
        user_to_delete = next((u for u in self.users if u.username == username), None)

        if user_to_delete and user_to_delete.role == 'admin' and admin_count <= 1:
            return False, "Cannot delete the last admin user"

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM users WHERE username = %s", (username,))
            conn.commit()
            conn.close()
            self.load_users()
            return True, "User deleted successfully"
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False, f"Error: {e}"

    def search_users(self, search_term):
        """Search users by username"""
        if not search_term:
            return self.users
        return [u for u in self.users if search_term.lower() in u.username.lower()]

    def add_product(self, name, price, stock):
        """Add product to MySQL database"""
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)",
                (name, price, stock)
            )
            conn.commit()
            conn.close()
            self.load_products()
            return True
        except Exception as e:
            print(f"Error adding product: {e}")
            return False

    def delete_product(self, product_id):
        """Delete a product by ID"""
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM products WHERE id = %s", (product_id,))
            conn.commit()
            conn.close()
            self.load_products()
            return True
        except Exception as e:
            print(f"Error deleting product: {e}")
            return False

    def search_products(self, search_term):
        """Search products by name"""
        if not search_term:
            return self.products
        return [p for p in self.products if search_term.lower() in p.name.lower()]

    def add_to_cart(self, product, quantity):
        if product.stock < quantity:
            return False
        for item in self.cart:
            if item.product.id == product.id:
                if item.quantity + quantity > product.stock:
                    return False
                item.quantity += quantity
                return True
        self.cart.append(CartItem(product, quantity))
        return True

    def remove_from_cart(self, index):
        if 0 <= index < len(self.cart):
            self.cart.pop(index)

    def clear_cart(self):
        self.cart = []

    def get_cart_total(self):
        return sum(item.get_total() for item in self.cart)

    def complete_sale(self):
        """Complete sale and record transaction in MySQL (normalized schema)"""
        if not self.cart or not self.current_user:
            return False

        try:
            conn = get_connection()
            cur = conn.cursor()

            # Get next order ID
            cur.execute("SELECT COUNT(*) FROM transactions")
            count = cur.fetchone()[0]
            order_id = f"OR{count + 1:04d}"

            # Prepare items list
            items = []
            for cart_item in self.cart:
                items.append({
                    'product_id': cart_item.product.id,
                    'product_name': cart_item.product.name,
                    'quantity': cart_item.quantity,
                    'price': cart_item.product.price
                })

            # Insert transaction into transactions table
            cur.execute(
                "INSERT INTO transactions (order_id, staff_name, total_amount, date) "
                "VALUES (%s, %s, %s, %s)",
                (
                    order_id,
                    self.current_user.username,
                    self.get_cart_total(),
                    datetime.now().strftime("%m-%d-%Y %I:%M %p")
                )
            )

            # Get the auto-generated transaction ID
            transaction_id = cur.lastrowid

            # Insert each item into transaction_items table
            for item in items:
                cur.execute(
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

                # Update stock for each product
                cur.execute(
                    "UPDATE products SET stock = stock - %s WHERE id = %s",
                    (item["quantity"], item["product_id"])
                )

            conn.commit()
            conn.close()

            # Clear cart
            self.cart = []

            # Reload data from database
            self.load_products()
            self.load_transactions()

            print(f"Transaction saved: {order_id}")
            print(f"Total transactions: {len(self.transactions)}")

            return True
        except Exception as e:
            print(f"Error completing sale: {e}")
            import traceback
            traceback.print_exc()
            return False

    def search_transactions(self, search_term):
        """Search transactions by order ID or staff name"""
        if not search_term:
            return self.transactions
        search_term = search_term.lower()
        return [t for t in self.transactions
                if search_term in t.order_id.lower()
                or search_term in t.staff_name.lower()]