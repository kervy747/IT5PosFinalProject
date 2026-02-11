import logging
from Model.product import Product
from Controller.db import get_connection

logger = logging.getLogger(__name__)

class ProductOperations:

    def load_products(self):
        try:
            conn = get_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT product_id, name, price, stock FROM products")
            rows = cur.fetchall()

            self.products = [Product(row['product_id'], row['name'], row['price'], row['stock']) for row in rows]

            conn.close()
            logger.info(f"Loaded {len(self.products)} products from database")
        except Exception as e:
            logger.error(f"Error loading products: {e}")
            self.products = []

    def add_product(self, name, price, stock):
        try:
            conn = get_connection()
            cur = conn.cursor()

            # Check if product with same name already exists
            cur.execute("SELECT product_id, stock FROM products WHERE name = %s", (name,))
            existing = cur.fetchone()

            if existing:
                # Product exists - update stock
                cur.execute(
                    "UPDATE products SET stock = stock + %s WHERE product_id = %s",
                    (stock, existing[0])
                )
                product_id = existing[0]
                logger.info(f"Updated stock for existing product '{name}' (ID: {product_id})")
            else:
                # New product - generate ID and insert
                product_id = self._generate_next_product_id(cur)
                cur.execute(
                    "INSERT INTO products (product_id, name, price, stock) VALUES (%s, %s, %s, %s)",
                    (product_id, name, price, stock)
                )
                logger.info(f"Created new product '{name}' (ID: {product_id})")

            conn.commit()
            conn.close()

            self.load_products()
            return True, product_id
        except Exception as e:
            logger.error(f"Error adding product '{name}': {e}")
            return False, None

    def delete_product(self, product_id):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
            conn.commit()
            conn.close()

            self.load_products()
            logger.info(f"Product '{product_id}' deleted successfully")
            return True, "Product deleted successfully"
        except Exception as e:
            logger.error(f"Error deleting product '{product_id}': {e}")
            return False, f"Error: {e}"

    def search_products(self, search_term):
        if not search_term:
            return self.products

        search_lower = search_term.lower()
        return [p for p in self.products
                if search_lower in p.name.lower()
                or search_lower in p.product_id.lower()]