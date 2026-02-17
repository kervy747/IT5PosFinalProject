from PyQt6.QtWidgets import QMessageBox

class ProductController:
    def __init__(self, main_controller):
        self.main = main_controller
        self.model = main_controller.model
        self.main_window = main_controller.main_window

    def handle_add_product(self, name, price, stock):
        success, product_id = self.model.add_product(name, price, stock)

        if success:
            QMessageBox.information(self.main_window, "Success", f"Product saved successfully (ID: {product_id})")
        else:
            QMessageBox.warning(self.main_window, "Error", "Failed to add product. Check the console for details.")

        self.main.admin_tabbed_view.update_products_table(self.model.products)
        self.main.pos_view.update_products(self.model.products)

    def handle_delete_product(self, product_id):
        reply = QMessageBox.question(
            self.main_window,
            "Confirm Delete",
            f"Are you sure you want to delete product {product_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # FIXED: delete_product returns a tuple (success, message) — unpack it
            success, message = self.model.delete_product(product_id)

            if success:
                QMessageBox.information(self.main_window, "Success", "Product deleted successfully")
            else:
                QMessageBox.warning(self.main_window, "Error", f"Failed to delete: {message}")

            self.main.admin_tabbed_view.update_products_table(self.model.products)
            self.main.pos_view.update_products(self.model.products)

    def handle_search_products(self, search_term):
        filtered_products = self.model.search_products(search_term)
        self.main.admin_tabbed_view.update_products_table(filtered_products)