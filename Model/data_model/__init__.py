from .base import DataModel as BaseDataModel
from .user_operations import UserOperations
from .product_operations import ProductOperations
from .cart_operations import CartOperations
from .transaction_operations import TransactionOperations


class DataModel(BaseDataModel, UserOperations, ProductOperations, CartOperations, TransactionOperations):
    pass
# Export the complete DataModel class
__all__ = ['DataModel']
