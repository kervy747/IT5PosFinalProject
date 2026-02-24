import logging

logger = logging.getLogger(__name__)


class ProductOperations:

    def search_products(self, search_term):
        if not search_term:
            return self.products

        search_lower = search_term.lower()
        return [p for p in self.products
                if search_lower in p.name.lower()
                or search_lower in p.product_id.lower()]