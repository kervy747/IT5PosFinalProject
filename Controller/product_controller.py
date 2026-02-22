class ProductController:
    def __init__(self, main_controller):
        self.main = main_controller
        self.model = main_controller.model
        self.main_window = main_controller.main_window

    def handle_add_product(self, name, price, stock):
        success, product_id = self.model.add_product(name, price, stock)

        if success:
            self.main.admin_tabbed_view.product_mgmt_tab.show_info("Success", f"Product saved successfully (ID: {product_id})")
        else:
            self.main.admin_tabbed_view.product_mgmt_tab.show_error("Error", "Failed to add product. Check the console for details.")

        self.main.admin_tabbed_view.update_products_table(self.model.products)
        self.main.pos_view.update_products(self.model.products)

    def handle_delete_product(self, product_id):
        confirmed = self.main.admin_tabbed_view.product_mgmt_tab.show_question(
            "Confirm Delete",
            f"Are you sure you want to delete product {product_id}?"
        )

        if confirmed:
            success, message = self.model.delete_product(product_id)

            if success:
                self.main.admin_tabbed_view.product_mgmt_tab.show_info("Success", "Product deleted successfully")
            else:
                self.main.admin_tabbed_view.product_mgmt_tab.show_error("Error", f"Failed to delete: {message}")

            self.main.admin_tabbed_view.update_products_table(self.model.products)
            self.main.pos_view.update_products(self.model.products)

    def handle_search_products(self, search_term):
        filtered_products = self.model.search_products(search_term)
        self.main.admin_tabbed_view.update_products_table(filtered_products)