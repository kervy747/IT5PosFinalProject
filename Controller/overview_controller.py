from datetime import datetime

class OverviewController:
    def __init__(self, data_model):
         self.data_model = data_model

    def get_dashboard_data(self, selected_month=None, selected_year=None):
        transactions = self.data_model.transactions
        products = self.data_model.products

        if selected_month is None or selected_year is None:
            now = datetime.now()
            selected_month = now.month
            selected_year = now.year

        revenue_metrics = self._calculate_revenue_metrics(
            transactions, selected_month, selected_year
        )

        top_products = self._calculate_top_products(
            transactions, selected_month, selected_year
        )

        inventory_stats = self._calculate_inventory_stats(products)

        stock_alerts = self._get_stock_alerts(products)

        return {
            'revenue_metrics': revenue_metrics,
            'top_products': top_products,
            'inventory_stats': inventory_stats,
            'stock_alerts': stock_alerts,
            'selected_month': selected_month,
            'selected_year': selected_year
        }

    def _calculate_revenue_metrics(self, transactions, selected_month, selected_year):
        now = datetime.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        # Start of selected month
        month_start = datetime(selected_year, selected_month, 1, 0, 0, 0)

        # End of selected month
        if selected_month == 12:
            month_end = datetime(selected_year + 1, 1, 1, 0, 0, 0)
        else:
            month_end = datetime(selected_year, selected_month + 1, 1, 0, 0, 0)

        today_revenue = 0
        monthly_revenue = 0
        monthly_transactions = 0
        total_transactions = len(transactions)

        for transaction in transactions:
            trans_date = self._get_transaction_date(transaction)

            if trans_date:
                # Today's revenue (only for current date)
                if trans_date >= today_start and trans_date.date() == now.date():
                    today_revenue += transaction.total_amount

                # Monthly revenue (for selected month)
                if month_start <= trans_date < month_end:
                    monthly_revenue += transaction.total_amount
                    monthly_transactions += 1

        # Calculate average transaction for selected month
        avg_transaction = (
            monthly_revenue / monthly_transactions
            if monthly_transactions > 0
            else 0
        )

        return {
            'today_revenue': today_revenue,
            'monthly_revenue': monthly_revenue,
            'total_transactions': total_transactions,
            'monthly_transactions': monthly_transactions,
            'avg_transaction': avg_transaction
        }

    def _get_transaction_date(self, transaction):
        try:
            if hasattr(transaction, 'created_at') and transaction.created_at:
                return transaction.created_at
            elif hasattr(transaction, 'date') and transaction.date:
                return datetime.strptime(transaction.date, "%m-%d-%Y %I:%M %p")
        except Exception as e:
            print(f"Error parsing transaction date: {e}")

        return None

    def _calculate_top_products(self, transactions, selected_month, selected_year, limit=5):
        # Start and end of selected month
        month_start = datetime(selected_year, selected_month, 1, 0, 0, 0)

        if selected_month == 12:
            month_end = datetime(selected_year + 1, 1, 1, 0, 0, 0)
        else:
            month_end = datetime(selected_year, selected_month + 1, 1, 0, 0, 0)

        product_data = {}

        for transaction in transactions:
            trans_date = self._get_transaction_date(transaction)

            # Only include transactions from selected month
            if not trans_date or not (month_start <= trans_date < month_end):
                continue

            for item in transaction.items:
                # Handle both dict and object item formats
                if isinstance(item, dict):
                    product_name = item.get('product_name', 'Unknown')
                    quantity = item.get('quantity', 0)
                    price = item.get('price', 0)
                else:
                    product_name = getattr(item, 'product_name', 'Unknown')
                    quantity = getattr(item, 'quantity', 0)
                    price = getattr(item, 'price', 0)

                # Aggregate product data
                if product_name not in product_data:
                    product_data[product_name] = {'quantity': 0, 'revenue': 0}

                product_data[product_name]['quantity'] += quantity
                product_data[product_name]['revenue'] += quantity * price

        top_products = sorted(
            product_data.items(),
            key=lambda x: x[1]['quantity'],
            reverse=True
        )[:limit]

        return top_products

    def _calculate_inventory_stats(self, products):
        total_products = len(products)
        total_stock = sum(p.stock for p in products)

        low_stock_items = [p for p in products if 0 < p.stock <= 10]
        out_of_stock_items = [p for p in products if p.stock == 0]

        return {
            'total_products': total_products,
            'total_stock': total_stock,
            'low_stock_count': len(low_stock_items),
            'out_of_stock_count': len(out_of_stock_items),
            'low_stock_items': low_stock_items,
            'out_of_stock_items': out_of_stock_items
        }

    def _get_stock_alerts(self, products):
        alerts = []

        # Get products sorted by stock level
        low_stock = sorted(
            [p for p in products if 0 < p.stock <= 10],
            key=lambda p: p.stock
        )

        out_of_stock = sorted(
            [p for p in products if p.stock == 0],
            key=lambda p: p.name
        )

        # Add out of stock alerts (critical)
        for product in out_of_stock:
            alerts.append({
                'type': 'critical',
                'icon': '🔴',
                'message': f"{product.name} - OUT OF STOCK"
            })

        # Add low stock alerts (warning)
        for product in low_stock:
            alerts.append({
                'type': 'warning',
                'icon': '🟡',
                'message': f"{product.name} - {product.stock} units left"
            })

        # Add success message if no alerts
        if not alerts:
            alerts.append({
                'type': 'success',
                'icon': '✅',
                'message': 'All products are well stocked!'
            })

        return alerts

    def get_revenue_trend(self, days=7):
        transactions = self.data_model.transactions
        now = datetime.now()

        daily_revenue = {}

        for i in range(days):
            day = now.replace(hour=0, minute=0, second=0, microsecond=0)
            day = day.replace(day=day.day - i)
            daily_revenue[day.strftime("%Y-%m-%d")] = 0

        for transaction in transactions:
            trans_date = self._get_transaction_date(transaction)
            if trans_date:
                date_key = trans_date.strftime("%Y-%m-%d")
                if date_key in daily_revenue:
                    daily_revenue[date_key] += transaction.total_amount
        return daily_revenue

    def get_product_performance(self, product_name):
        transactions = self.data_model.transactions

        total_quantity = 0
        total_revenue = 0
        transaction_count = 0

        for transaction in transactions:
            for item in transaction.items:
                # Handle both dict and object item formats
                if isinstance(item, dict):
                    name = item.get('product_name', '')
                    quantity = item.get('quantity', 0)
                    price = item.get('price', 0)
                else:
                    name = getattr(item, 'product_name', '')
                    quantity = getattr(item, 'quantity', 0)
                    price = getattr(item, 'price', 0)

                if name == product_name:
                    total_quantity += quantity
                    total_revenue += quantity * price
                    transaction_count += 1

        avg_quantity = total_quantity / transaction_count if transaction_count > 0 else 0

        return {
            'total_quantity_sold': total_quantity,
            'total_revenue': total_revenue,
            'transaction_count': transaction_count,
            'avg_quantity_per_transaction': avg_quantity
        }