from datetime import datetime
import os

class ReceiptGenerator:
    def __init__(self, receipt_folder="receipts"):
        self.receipt_folder = receipt_folder
        self._ensure_receipt_folder_exists()

    def _ensure_receipt_folder_exists(self):
        if not os.path.exists(self.receipt_folder):
            os.makedirs(self.receipt_folder)
            print(f"Created receipts folder: {self.receipt_folder}")

    def generate_receipt(self, order_id, staff_name, cart_items, total_amount, cash_amount, change_amount, transaction_date=None):
        try:
            if transaction_date is None:
                transaction_date = datetime.now().strftime("%m-%d-%Y %I:%M %p")

            # Generate receipt content
            receipt_text = self._format_receipt(
                order_id, staff_name, cart_items, total_amount,
                cash_amount, change_amount, transaction_date
            )

            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{order_id}_{timestamp}.txt"
            filepath = os.path.join(self.receipt_folder, filename)

            # Save to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(receipt_text)

            print(f"✓ Receipt saved: {filepath}")
            return True, filepath

        except Exception as e:
            error_msg = f"Error generating receipt: {str(e)}"
            print(f"✗ {error_msg}")
            import traceback
            traceback.print_exc()
            return False, error_msg

    def _format_receipt(self, order_id, staff_name, cart_items, total_amount, cash_amount, change_amount, transaction_date):
        # Dynamically calculate name column based on longest product name
        longest_name = max((len(item.product.name) for item in cart_items), default=20)
        name_col = max(longest_name + 2, 22)  # at least 22, or longest name + 2 padding
        # Total width = name_col + QTY(5) + PRICE(12) + TOTAL(12) + 3 spaces between
        width = name_col + 5 + 12 + 12 + 3

        # Build receipt line by line
        lines = []

        # Header
        lines.append("=" * width)
        lines.append(self._center_text("Terminal 360", width))
        lines.append(self._center_text("Point of Sale System", width))
        lines.append("=" * width)
        lines.append("")

        # Transaction info
        lines.append(f"Receipt No: {order_id}")
        lines.append(f"Date: {transaction_date}")
        lines.append(f"Cashier: {staff_name}")
        lines.append("-" * width)
        lines.append("")

        # Items header
        lines.append(f"{'ITEM':<{name_col}} {'QTY':>5} {'PRICE':>12} {'TOTAL':>12}")
        lines.append("-" * width)

        # Items — full product name, no truncation
        for item in cart_items:
            product_name = item.product.name
            qty = str(item.quantity)
            price = f"₱{item.product.price:,.2f}"
            item_total = f"₱{item.get_total():,.2f}"

            lines.append(f"{product_name:<{name_col}} {qty:>5} {price:>12} {item_total:>12}")

        lines.append("-" * width)
        lines.append("")

        # Totals
        lines.append(self._right_align(f"SUBTOTAL: ₱{total_amount:,.2f}", width))
        lines.append(self._right_align(f"TOTAL:    ₱{total_amount:,.2f}", width))
        lines.append("")
        lines.append(self._right_align(f"CASH:     ₱{cash_amount:,.2f}", width))
        lines.append(self._right_align(f"CHANGE:   ₱{change_amount:,.2f}", width))
        lines.append("")

        # Footer
        lines.append("=" * width)
        lines.append(self._center_text("Thank you for your purchase!", width))
        lines.append(self._center_text("Please come again!", width))
        lines.append("=" * width)
        lines.append("")
        lines.append(self._center_text("Powered by Terminal 360", width))
        lines.append("")

        return "\n".join(lines)

    def _center_text(self, text, width):
        return text.center(width)

    def _right_align(self, text, width):
        return text.rjust(width)

    def _format_line(self, col1, col2, col3, col4, width):
        # Column widths: Item(20), Qty(5), Price(10), Total(10)
        return f"{col1:<20} {col2:>5} {col3:>10} {col4:>10}"

    def _format_item_line(self, name, qty, price, total, width):
        return f"{name:<20} {qty:>5} {price:>10} {total:>10}"

    def open_receipt(self, filepath):
        try:
            import platform
            import subprocess

            system = platform.system()

            if system == "Windows":
                os.startfile(filepath)
            elif system == "Darwin":  # macOS
                subprocess.call(["open", filepath])
            else:  # Linux
                subprocess.call(["xdg-open", filepath])

            return True
        except Exception as e:
            print(f"Error opening receipt: {e}")
            return False