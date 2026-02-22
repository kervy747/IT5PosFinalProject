from datetime import datetime


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

    def handle_filter_by_month(self, month, year):
        filtered = []
        for t in self.model.transactions:
            try:
                trans_date = datetime.strptime(t.date, "%m-%d-%Y %I:%M %p")
                if trans_date.month == month and trans_date.year == year:
                    filtered.append(t)
            except Exception:
                pass
        self.main.admin_tabbed_view.transactions_tab.month_selector.set_available_years(self.model.transactions)
        self.main.admin_tabbed_view.update_transactions_table(filtered)

    def handle_delete_transaction(self, order_id):
        confirmed = self.main.admin_tabbed_view.transactions_tab.show_question(
            "Confirm Delete",
            f"Are you sure you want to delete transaction '{order_id}'?\n\n"
            "This action cannot be undone."
        )

        if confirmed:
            success, message = self.model.delete_transaction(order_id)
            if success:
                self.main.admin_tabbed_view.transactions_tab.show_info("Success", message)
                self.main.transaction_view.update_transactions_table(self.model.transactions)
                if hasattr(self.main, 'overview_view'):
                    self.main.overview_view.update_overview(self.model.transactions, self.model.products)
            else:
                self.main.admin_tabbed_view.transactions_tab.show_error("Error", message)