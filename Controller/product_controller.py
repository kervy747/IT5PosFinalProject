import logging
from Controller.db import get_connection
from Model.product import Product

logger = logging.getLogger(__name__)


class ProductController:
    def __init__(self, main_controller):
        self.main = main_controller
        self.model = main_controller.model
        self.main_window = main_controller.main_window

    def load_products(self):
        try:
            conn = get_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT product_id, name, price, stock FROM products")
            rows = cur.fetchall()

            self.model.products = [Product(row['product_id'], row['name'], row['price'], row['stock']) for row in rows]

            conn.close()
            logger.info(f"Loaded {len(self.model.products)} products from database")
        except Exception as e:
            logger.error(f"Error loading products: {e}")
            self.model.products = []

    def _generate_next_product_id(self, cursor):
        cursor.execute("SELECT setting_value FROM system_settings WHERE setting_key = 'next_product_number'")
        result = cursor.fetchone()

        if result:
            next_number = int(result[0])
        else:
            next_number = 1
            cursor.execute(
                "INSERT INTO system_settings (setting_key, setting_value) VALUES ('next_product_number', '1')"
            )

        product_id = f"PR{next_number:05d}"

        cursor.execute(
            "UPDATE system_settings SET setting_value = %s WHERE setting_key = 'next_product_number'",
            (next_number + 1,)
        )

        return product_id

    def handle_add_product(self, name, price, stock):
        try:
            conn = get_connection()
            cur = conn.cursor()

            cur.execute("SELECT product_id, stock FROM products WHERE name = %s", (name,))
            existing = cur.fetchone()

            if existing:
                cur.execute(
                    "UPDATE products SET stock = stock + %s WHERE product_id = %s",
                    (stock, existing[0])
                )
                product_id = existing[0]
                logger.info(f"Updated stock for existing product '{name}' (ID: {product_id})")
            else:
                product_id = self._generate_next_product_id(cur)
                cur.execute(
                    "INSERT INTO products (product_id, name, price, stock) VALUES (%s, %s, %s, %s)",
                    (product_id, name, price, stock)
                )
                logger.info(f"Created new product '{name}' (ID: {product_id})")

            conn.commit()
            conn.close()

            self.load_products()
            self.main.admin_tabbed_view.product_mgmt_tab.show_info("Success", f"Product saved successfully (ID: {product_id})")
        except Exception as e:
            logger.error(f"Error adding product '{name}': {e}")
            self.main.admin_tabbed_view.product_mgmt_tab.show_error("Error", "Failed to add product. Check the console for details.")

        self.main.admin_tabbed_view.update_products_table(self.model.products)
        self.main.pos_view.update_products(self.model.products)

    def handle_delete_product(self, product_id):
        confirmed = self.main.admin_tabbed_view.product_mgmt_tab.show_question(
            "Confirm Delete",
            f"Are you sure you want to delete product {product_id}?"
        )

        if confirmed:
            try:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
                conn.commit()
                conn.close()

                self.load_products()
                logger.info(f"Product '{product_id}' deleted successfully")
                self.main.admin_tabbed_view.product_mgmt_tab.show_info("Success", "Product deleted successfully")
            except Exception as e:
                logger.error(f"Error deleting product '{product_id}': {e}")
                self.main.admin_tabbed_view.product_mgmt_tab.show_error("Error", f"Failed to delete: {e}")

            self.main.admin_tabbed_view.update_products_table(self.model.products)
            self.main.pos_view.update_products(self.model.products)

    def handle_search_products(self, search_term):
        filtered_products = self.model.search_products(search_term)
        self.main.admin_tabbed_view.update_products_table(filtered_products)