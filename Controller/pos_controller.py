from PyQt6.QtWidgets import QMessageBox
from receipt_generator import ReceiptGenerator

class POSOperationsController:
    def __init__(self, main_controller):
        self.main = main_controller
        self.model = main_controller.model
        self.main_window = main_controller.main_window

        # Initialize receipt generator
        self.receipt_generator = ReceiptGenerator(receipt_folder="receipts")

    def handle_add_to_cart(self, product_id, quantity):
        # Find product by product_id (now string format)
        product = next((p for p in self.model.products if p.product_id == product_id), None)

        if product:
            if self.model.add_to_cart(product, quantity):
                # ✅ Filter products before sending to view
                available_products = self._get_available_products()
                self.main.pos_view.update_products(available_products)
                self.main.pos_view.update_cart(self.model.cart, self.model.get_cart_total())
            else:
                QMessageBox.warning(self.main_window, "Error", "Insufficient stock")
        else:
            QMessageBox.warning(self.main_window, "Error", f"Product {product_id} not found")

    def handle_remove_from_cart(self, index):
        self.model.remove_from_cart(index)
        # ✅ Filter products before sending to view
        available_products = self._get_available_products()
        self.main.pos_view.update_products(available_products)
        self.main.pos_view.update_cart(self.model.cart, self.model.get_cart_total())

    def handle_complete_sale(self):
        try:
            if not self.model.cart:
                QMessageBox.warning(self.main_window, "Error", "Cart is empty")
                return

            cash_amount = self.main.pos_view.cart_view.get_cash_amount()

            if cash_amount is None:
                QMessageBox.warning(self.main_window, "Error", "Please enter cash amount")
                self.main.pos_view.cart_view.cash_input.setFocus()
                return

            total = float(self.model.get_cart_total())

            if cash_amount < total:
                shortage = total - cash_amount
                QMessageBox.warning(
                    self.main_window,
                    "Insufficient Cash",
                    f"Cash is short by ₱{shortage:,.2f}"
                )
                self.main.pos_view.cart_view.cash_input.setFocus()
                return

            change = cash_amount - total

            reply = QMessageBox.question(
                self.main_window,
                "Confirm Sale",
                f"Total: ₱{total:,.2f}\n"
                f"Cash: ₱{cash_amount:,.2f}\n"
                f"Change: ₱{change:,.2f}\n\n"
                f"Complete this sale?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.Yes
            )

            if reply == QMessageBox.StandardButton.Yes:
                cart_items_copy = self.model.cart.copy()
                staff_name = self.model.current_user.username if self.model.current_user else "Unknown"

                try:
                    self.model.complete_sale()
                except Exception as e:
                    print(f"Error in model.complete_sale(): {e}")
                    import traceback
                    traceback.print_exc()
                    QMessageBox.critical(self.main_window, "Error", f"Failed to complete sale: {str(e)}")
                    return

                if self.model.transactions:
                    last_transaction = self.model.transactions[0]  # Transactions are ordered DESC
                    order_id = last_transaction.order_id
                else:
                    order_id = "OR?????"  # Fallback

                # ✅ Update views with filtered products
                try:
                    available_products = self._get_available_products()
                    self.main.pos_view.update_products(available_products)
                    self.main.pos_view.update_cart(self.model.cart, self.model.get_cart_total())
                except Exception as e:
                    print(f"Error updating views: {e}")
                    import traceback
                    traceback.print_exc()

                try:
                    self.main.pos_view.cart_view.clear_cash_input()
                except Exception as e:
                    print(f"Error clearing cash input: {e}")

                self._generate_and_show_receipt(
                    order_id, staff_name, cart_items_copy,
                    total, cash_amount, change
                )

        except Exception as e:
            print(f"FATAL ERROR in handle_complete_sale: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_window, "Critical Error",
                                 f"An unexpected error occurred: {str(e)}")

    def _get_available_products(self):
        """
        ✅ NEW: Filter products to only show items with stock > 0
        This logic was moved from the view to the controller
        """
        return [p for p in self.model.products if p.stock > 0]

    def _generate_and_show_receipt(self, order_id, staff_name, cart_items, total, cash_amount, change):
        try:
            # Generate receipt
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

                # Show success message with receipt options
                msg = QMessageBox(self.main_window)
                msg.setIcon(QMessageBox.Icon.Information)
                msg.setWindowTitle("Sale Completed")
                msg.setText(
                    f"Sale completed successfully!\n\n"
                    f"Order ID: {order_id}\n"
                    f"Total: ₱{total:,.2f}\n"
                    f"Cash: ₱{cash_amount:,.2f}\n"
                    f"Change: ₱{change:,.2f}\n\n"
                    f"Receipt saved to:\n{filepath}"
                )

                # Add custom buttons
                open_btn = msg.addButton("Open Receipt", QMessageBox.ButtonRole.AcceptRole)
                close_btn = msg.addButton("Close", QMessageBox.ButtonRole.RejectRole)

                msg.exec()

                if msg.clickedButton() == open_btn:
                    self.receipt_generator.open_receipt(filepath)

            else:
                QMessageBox.warning(
                    self.main_window,
                    "Receipt Error",
                    f"Sale completed successfully!\n\n"
                    f"Order ID: {order_id}\n"
                    f"Total: ₱{total:,.2f}\n"
                    f"Cash: ₱{cash_amount:,.2f}\n"
                    f"Change: ₱{change:,.2f}\n\n"
                    f"However, receipt generation failed:\n{result}"
                )

        except Exception as e:
            print(f"Error generating receipt: {e}")
            import traceback
            traceback.print_exc()

            QMessageBox.information(
                self.main_window,
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