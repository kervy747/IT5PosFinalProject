"""
POS (Point of Sale) Controller
Handles cart and sales operations
"""
from PyQt6.QtWidgets import QMessageBox


class POSOperationsController:
    """Handles POS operations like cart management and sales"""

    def __init__(self, main_controller):
        self.main = main_controller
        self.model = main_controller.model
        self.main_window = main_controller.main_window

    def handle_add_to_cart(self, product_id, quantity):
        """Add product to cart"""
        product = next((p for p in self.model.products if p.id == product_id), None)
        if product:
            if self.model.add_to_cart(product, quantity):
                self.main.pos_view.update_cart(self.model.cart, self.model.get_cart_total())
            else:
                QMessageBox.warning(self.main_window, "Error", "Insufficient stock")

    def handle_remove_from_cart(self, index):
        """Remove item from cart"""
        self.model.remove_from_cart(index)
        self.main.pos_view.update_cart(self.model.cart, self.model.get_cart_total())

    def handle_complete_sale(self):
        """Handle sale completion - validation already done in cart view"""
        try:
            # Check if cart is empty
            if not self.model.cart:
                QMessageBox.warning(self.main_window, "Error", "Cart is empty")
                return

            # Get cash amount (already validated in cartView)
            try:
                cash_text = self.main.pos_view.cart_view.cash_input.text().strip()
                cash_amount = float(cash_text)
            except (ValueError, AttributeError) as e:
                print(f"Error getting cash amount: {e}")
                QMessageBox.warning(self.main_window, "Error", "Invalid cash amount")
                return

            total = float(self.model.get_cart_total())
            change = cash_amount - total

            # Final confirmation with details
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
                # Complete the sale
                try:
                    self.model.complete_sale()
                except Exception as e:
                    print(f"Error in model.complete_sale(): {e}")
                    import traceback
                    traceback.print_exc()
                    QMessageBox.critical(self.main_window, "Error", f"Failed to complete sale: {str(e)}")
                    return

                # Update views
                try:
                    self.main.pos_view.update_products(self.model.products)
                    self.main.pos_view.update_cart(self.model.cart, self.model.get_cart_total())
                except Exception as e:
                    print(f"Error updating views: {e}")
                    import traceback
                    traceback.print_exc()

                # Clear cash input after successful sale
                try:
                    self.main.pos_view.cart_view.clear_cash_input()
                except Exception as e:
                    print(f"Error clearing cash input: {e}")

                # Show success message with change
                try:
                    QMessageBox.information(
                        self.main_window,
                        "Sale Completed",
                        f"Sale completed successfully!\n\n"
                        f"Total: ₱{total:,.2f}\n"
                        f"Cash: ₱{cash_amount:,.2f}\n"
                        f"Change: ₱{change:,.2f}"
                    )
                except Exception as e:
                    print(f"Error showing success message: {e}")
                    import traceback
                    traceback.print_exc()

        except Exception as e:
            print(f"FATAL ERROR in handle_complete_sale: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_window, "Critical Error",
                                 f"An unexpected error occurred: {str(e)}")