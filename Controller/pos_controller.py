import logging
from datetime import datetime
from Controller.db import get_connection
from receipt_generator import ReceiptGenerator
logger = logging.getLogger(__name__)

class POSOperationsController:
    def __init__(self, main_controller):
        self.main = main_controller
        self.model = main_controller.model
        self.main_window = main_controller.main_window

        self.receipt_generator = ReceiptGenerator(receipt_folder="receipts")

    def handle_add_to_cart(self, product_id, quantity):
        product = next((p for p in self.model.products if p.product_id == product_id), None)

        if product:
            if self.model.add_to_cart(product, quantity):
                available_products = self._get_available_products()
                self.main.pos_view.update_products(available_products)
                self.main.pos_view.update_cart(self.model.cart, self.model.get_cart_total())
            else:
                self.main.pos_view.show_error("Error", "Insufficient stock")
        else:
            self.main.pos_view.show_error("Error", f"Product {product_id} not found")

    def handle_remove_from_cart(self, index):
        self.model.remove_from_cart(index)

        available_products = self._get_available_products()
        self.main.pos_view.update_products(available_products)
        self.main.pos_view.update_cart(self.model.cart, self.model.get_cart_total())

    def handle_complete_sale(self):
        try:
            if not self.model.cart:
                self.main.pos_view.show_error("Error", "Cart is empty")
                return

            cash_amount = self.main.pos_view.cart_view.get_cash_amount()

            if cash_amount is None:
                self.main.pos_view.show_error("Error", "Please enter cash amount")
                self.main.pos_view.cart_view.cash_input.setFocus()
                return

            total = float(self.model.get_cart_total())

            if cash_amount < total:
                shortage = total - cash_amount
                self.main.pos_view.show_error(
                    "Insufficient Cash",
                    f"Cash is short by ₱{shortage:,.2f}"
                )
                self.main.pos_view.cart_view.cash_input.setFocus()
                return

            change = cash_amount - total

            confirmed = self.main.pos_view.show_question(
                "Confirm Sale",
                f"Total: ₱{total:,.2f}\n"
                f"Cash: ₱{cash_amount:,.2f}\n"
                f"Change: ₱{change:,.2f}\n\n"
                f"Complete this sale?"
            )

            if confirmed:
                cart_items_copy = self.model.cart.copy()
                current_user = self.main.auth.get_current_user()
                staff_name = current_user.username if current_user else "Unknown"

                try:
                    success, order_id = self._complete_sale_db(current_user)

                    if not success:
                        self.main.pos_view.show_error("Error", "Failed to complete sale. Please try again.")
                        return

                except Exception as e:
                    logger.error(f"Error in _complete_sale_db: {e}")
                    import traceback
                    traceback.print_exc()
                    self.main.pos_view.show_error("Error", f"Failed to complete sale: {str(e)}")
                    return

                try:
                    available_products = self._get_available_products()
                    self.main.pos_view.update_products(available_products)
                    self.main.pos_view.update_cart(self.model.cart, self.model.get_cart_total())
                except Exception as e:
                    logger.error(f"Error updating views: {e}")
                    import traceback
                    traceback.print_exc()

                try:
                    self.main.pos_view.cart_view.clear_cash_input()
                except Exception as e:
                    logger.error(f"Error clearing cash input: {e}")

                self._generate_and_show_receipt(
                    order_id, staff_name, cart_items_copy,
                    total, cash_amount, change
                )

        except Exception as e:
            logger.error(f"FATAL ERROR in handle_complete_sale: {e}")
            import traceback
            traceback.print_exc()
            self.main.pos_view.show_error("Critical Error", f"An unexpected error occurred: {str(e)}")

    def _complete_sale_db(self, current_user):
        if not self.model.cart:
            return False, None

        if not current_user:
            return False, None

        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()

            order_id = self._generate_next_order_id(cur)

            items = [{
                'product_id': item.product.product_id,
                'product_name': item.product.name,
                'quantity': item.quantity,
                'price': item.product.price
            } for item in self.model.cart]

            cur.execute("SELECT id FROM users WHERE username = %s", (current_user.username,))
            result = cur.fetchone()
            if not result:
                raise ValueError(f"User '{current_user.username}' not found in database")
            user_id = result[0]

            cur.execute(
                "INSERT INTO transactions (order_id, user_id, staff_name, total_amount, date) "
                "VALUES (%s, %s, %s, %s, %s)",
                (
                    order_id,
                    user_id,
                    current_user.username,
                    self.model.get_cart_total(),
                    datetime.now().strftime("%m-%d-%Y %I:%M %p")
                )
            )
            transaction_id = cur.lastrowid

            for item in items:
                cur.execute(
                    "INSERT INTO transaction_items (transaction_id, product_id, product_name, quantity, price) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (transaction_id, item['product_id'], item['product_name'], item['quantity'], item['price'])
                )

            for item in items:
                cur.execute(
                    "UPDATE products SET stock = stock - %s WHERE product_id = %s",
                    (item["quantity"], item["product_id"])
                )

            conn.commit()
            logger.info(f"Sale completed successfully: {order_id}")

            self.model.clear_cart()
            self.main.product.load_products()
            self.main.transaction.load_transactions()

            return True, order_id

        except Exception as e:
            logger.error(f"Error completing sale: {e}")
            if conn:
                conn.rollback()
            return False, None
        finally:
            if conn:
                conn.close()

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

    def _get_available_products(self):
        return [p for p in self.model.products if p.stock > 0]

    def _generate_and_show_receipt(self, order_id, staff_name, cart_items, total, cash_amount, change):
        try:
            success, result = self.receipt_generator.generate_receipt(
                order_id=order_id,
                staff_name=staff_name,
                cart_items=cart_items,
                total_amount=total,
                cash_amount=cash_amount,
                change_amount=change
            )

            if success:
                filepath = result
                open_receipt = self.main.pos_view.show_sale_complete(
                    order_id, total, cash_amount, change, filepath
                )
                if open_receipt:
                    self.receipt_generator.open_receipt(filepath)
            else:
                self.main.pos_view.show_error(
                    "Receipt Error",
                    f"Sale completed successfully!\n\n"
                    f"Order ID: {order_id}\n"
                    f"Total: ₱{total:,.2f}\n"
                    f"Cash: ₱{cash_amount:,.2f}\n"
                    f"Change: ₱{change:,.2f}\n\n"
                    f"However, receipt generation failed:\n{result}"
                )

        except Exception as e:
            logger.error(f"Error generating receipt: {e}")
            import traceback
            traceback.print_exc()
            self.main.pos_view.show_info(
                "Sale Completed",
                f"Sale completed successfully!\n\n"
                f"Order ID: {order_id}\n"
                f"Total: ₱{total:,.2f}\n"
                f"Cash: ₱{cash_amount:,.2f}\n"
                f"Change: ₱{change:,.2f}\n\n"
                f"Note: Receipt could not be generated."
            )

    def refresh_products(self):
        available_products = self._get_available_products()
        self.main.pos_view.update_products(available_products)