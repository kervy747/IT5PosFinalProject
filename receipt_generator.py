"""
Receipt Generator Module
Generates formatted receipt text files for transactions
"""
from datetime import datetime
import os


class ReceiptGenerator:
    """Generates receipt text files for completed transactions"""

    def __init__(self, receipt_folder="receipts"):
        """
        Initialize receipt generator

        Args:
            receipt_folder: Folder to save receipts (default: "receipts")
        """
        self.receipt_folder = receipt_folder
        self._ensure_receipt_folder_exists()

    def _ensure_receipt_folder_exists(self):
        """Create receipts folder if it doesn't exist"""
        if not os.path.exists(self.receipt_folder):
            os.makedirs(self.receipt_folder)
            print(f"Created receipts folder: {self.receipt_folder}")

    def generate_receipt(self, order_id, staff_name, cart_items, total_amount,
                         cash_amount, change_amount, transaction_date=None):
        """
        Generate a formatted receipt and save to text file

        Args:
            order_id: Order ID (e.g., "OR0001")
            staff_name: Name of staff who processed the sale
            cart_items: List of cart items (CartItem objects)
            total_amount: Total sale amount
            cash_amount: Cash received
            change_amount: Change given
            transaction_date: Date/time of transaction (optional, defaults to now)

        Returns:
            tuple: (success: bool, filepath: str or error_message: str)
        """
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

    def _format_receipt(self, order_id, staff_name, cart_items, total_amount,
                        cash_amount, change_amount, transaction_date):
        """
        Format receipt content with proper alignment

        Returns:
            str: Formatted receipt text
        """
        width = 50  # Receipt width in characters

        # Build receipt line by line
        lines = []

        # Header
        lines.append("=" * width)
        lines.append(self._center_text("TECH 360", width))
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
        lines.append(self._format_line("ITEM", "QTY", "PRICE", "TOTAL", width))
        lines.append("-" * width)

        # Items
        for item in cart_items:
            product_name = item.product.name
            # Truncate name if too long
            if len(product_name) > 20:
                product_name = product_name[:17] + "..."

            qty = str(item.quantity)
            price = f"₱{item.product.price:,.2f}"
            item_total = f"₱{item.get_total():,.2f}"

            lines.append(self._format_item_line(product_name, qty, price, item_total, width))

        lines.append("-" * width)
        lines.append("")

        # Totals
        lines.append(self._right_align(f"SUBTOTAL: ₱{total_amount:,.2f}", width))
        lines.append(self._right_align(f"TOTAL: ₱{total_amount:,.2f}", width))
        lines.append("")
        lines.append(self._right_align(f"CASH: ₱{cash_amount:,.2f}", width))
        lines.append(self._right_align(f"CHANGE: ₱{change_amount:,.2f}", width))
        lines.append("")

        # Footer
        lines.append("=" * width)
        lines.append(self._center_text("Thank you for your purchase!", width))
        lines.append(self._center_text("Please come again!", width))
        lines.append("=" * width)
        lines.append("")
        lines.append(self._center_text("Powered by Tech 360 POS", width))
        lines.append("")

        return "\n".join(lines)

    def _center_text(self, text, width):
        """Center text within given width"""
        return text.center(width)

    def _right_align(self, text, width):
        """Right align text within given width"""
        return text.rjust(width)

    def _format_line(self, col1, col2, col3, col4, width):
        """Format a line with 4 columns"""
        # Column widths: Item(20), Qty(5), Price(10), Total(10)
        return f"{col1:<20} {col2:>5} {col3:>10} {col4:>10}"

    def _format_item_line(self, name, qty, price, total, width):
        """Format an item line"""
        return f"{name:<20} {qty:>5} {price:>10} {total:>10}"

    def open_receipt(self, filepath):
        """
        Open receipt file with default text editor

        Args:
            filepath: Path to receipt file

        Returns:
            bool: Success status
        """
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


# Example usage:
if __name__ == "__main__":
    # For testing
    class MockProduct:
        def __init__(self, product_id, name, price):
            self.product_id = product_id
            self.name = name
            self.price = price


    class MockCartItem:
        def __init__(self, product, quantity):
            self.product = product
            self.quantity = quantity

        def get_total(self):
            return self.product.price * self.quantity


    # Test data
    items = [
        MockCartItem(MockProduct("PR00001", "Intel Core i9-14900K CPU", 32999.00), 1),
        MockCartItem(MockProduct("PR00005", "Corsair Vengeance 32GB DDR5 RAM", 7299.00), 2),
        MockCartItem(MockProduct("PR00010", "EVGA SuperNOVA 850W PSU", 7349.00), 1),
    ]

    total = sum(item.get_total() for item in items)
    cash = 60000.00
    change = cash - total

    # Generate receipt
    generator = ReceiptGenerator()
    success, result = generator.generate_receipt(
        order_id="OR0001",
        staff_name="admin",
        cart_items=items,
        total_amount=total,
        cash_amount=cash,
        change_amount=change
    )

    if success:
        print(f"\n✓ Receipt generated successfully!")
        print(f"File: {result}")

        # Optionally open it
        generator.open_receipt(result)
    else:
        print(f"\n✗ Failed to generate receipt: {result}")