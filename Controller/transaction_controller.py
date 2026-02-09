from PyQt6.QtWidgets import QMessageBox

class TransactionController:
    def __init__(self, main_controller):
        self.main = main_controller
        self.model = main_controller.model
        self.main_window = main_controller.main_window

    def handle_view_transactions(self):
        self.main.transaction_view.update_transactions_table(self.model.transactions)
        self.main.stack.setCurrentWidget(self.main.transaction_view)

    def handle_search_transactions(self, search_term):
        filtered_transactions = self.model.search_transactions(search_term)
        self.main.admin_tabbed_view.update_transactions_table(filtered_transactions)

    def handle_delete_transaction(self, order_id):
        reply = QMessageBox.question(
            self.main_window,
            "Confirm Delete",
            f"Are you sure you want to delete transaction '{order_id}'?\n\n"
            "This action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success, message = self.model.delete_transaction(order_id)
            if success:
                QMessageBox.information(self.main_window, "Success", message)
                # Refresh the transactions table
                self.main.transaction_view.update_transactions_table(self.model.transactions)
                # Update overview if needed
                if hasattr(self.main, 'overview_view'):
                    self.main.overview_view.update_overview(self.model.transactions, self.model.products)
            else:
                QMessageBox.warning(self.main_window, "Error", message)