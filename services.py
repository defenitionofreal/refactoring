import datetime

from .validators import *
from .repos import *

class OrderListService:
    def __init__(self, user_id):
        self.user_id = user_id
        self._validator = OrderListValidator(self.user_id)
        self._repo = OrderListRepo(self.user_id)

    def _context(self) -> dict:
        order_ids = self._repo.orders.values_list('id', flat=True)
        return {
            'orders': self._repo.orders,
            'customers': self._repo.get_customer_lists(order_ids),
            'last_contact': self._repo.get_last_orders_comments(order_ids),
            'responsible_orders': self._repo.get_responsible_orders(order_ids),
            'favorites': self._repo.has_orders_favorites(order_ids),
            'tasks': self._repo.get_task_order_comments_num(order_ids)
        }

    def count(self, start: int = 0, stop: int = 0):
        self._validator.validate()
        return self._repo.get_search_orders(start, stop).count()

    def context(self, start: int = 0, stop: int = 0):
        self._validator.validate()
        self._repo.cached_orders(start, stop)
        return self._context()


class CostListService:
    def __init__(self, user_id):
        self.user_id = user_id
        self._validator = CostListValidator(self.user_id)
        self._repo = CostListRepo(self.user_id)

    def _context(self, start: int, stop: int) -> dict:
        return {
            'costs': self._repo.get_search_costs(start, stop),
            'approved_costs': self._repo.get_search_cost_approved_lists(start, stop),
            'today': datetime.date.today()
        }

    def count(self, start: int = 0, stop: int = 0):
        self._validator.validate()
        return self._repo.get_search_costs(start, stop).count()

    def context(self, start: int = 0, stop: int = 0):
        self._validator.validate()
        return self._context(start, stop)
