"""
Product Management Controller
Handles product CRUD operations
"""
from PyQt6.QtWidgets import QMessageBox


class ProductController:
    """Handles product management operations"""

    def __init__(self, main_controller):
        self.main = main_controller
        self.model = main_controller.model
        self.main_window = main_controller.main_window

    def handle_add_product(self, name, price, stock):
        """Add a new product"""
        self.model.add_product(name, price, stock)
        QMessageBox.information(self.main_window, "Success", "Product added successfully")
        self.main.admin_tabbed_view.update_products_table(self.model.products)
        self.main.pos_view.update_products(self.model.products)

    def handle_delete_product(self, product_id):
        """Delete a product with confirmation"""
        reply = QMessageBox.question(
            self.main_window,
            "Confirm Delete",
            f"Are you sure you want to delete this product?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.model.delete_product(product_id)
            QMessageBox.information(self.main_window, "Success", "Product deleted successfully")
            self.main.admin_tabbed_view.update_products_table(self.model.products)
            self.main.pos_view.update_products(self.model.products)

    def handle_search_products(self, search_term):
        """Search products by term"""
        filtered_products = self.model.search_products(search_term)
        self.main.admin_tabbed_view.update_products_table(filtered_products)