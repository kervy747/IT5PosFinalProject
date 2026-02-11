import sys
import os
import logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataModel:

    def __init__(self):
        self.users = []
        self.products = []
        self.transactions = []
        self.cart = []

        # Load all data from database
        self.load_users()
        self.load_products()
        self.load_transactions()

    # ==================== Helper Methods (Private) ====================

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