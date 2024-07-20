from typing import List, Dict

from django.db.models import QuerySet, Count

from prj.models import (
    Order, Search, OrderResponsible, CustomerList, Comments, Cost, ApprovedList,
    Favorites
)
from .filters import *


class OrderListRepo:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.orders = None

    def cached_orders(self, start: int, stop: int) -> QuerySet[Order]:
        if not self.orders:
            self.orders = self.get_search_orders(start, stop)

        return self.orders

    def is_existing_search(self) -> bool:
        return Search.objects.filter(user_id=self.user_id).exists()

    def get_user_search(self) -> Search:
        return Search.objects.get(user_id=self.user_id)

    def get_search_orders(self, start: int, stop: int) -> QuerySet[Order]:
        qs = Order.objects.prefetch_related('searchowners').filter(
            order_filter_by_search(self.get_user_search())
        ).order_by('-rating')

        if start and stop:
            return qs[(self.start - 1):self.stop]
        return qs

    def get_responsible_orders(self, order_ids: list) -> QuerySet[
        OrderResponsible]:
        return OrderResponsible.objects.filter(order_id__in=order_ids).order_by(
            'order_id')

    def get_customer_lists(self, order_ids: list) -> QuerySet[CustomerList]:
        return CustomerList.objects.filter(order_id=order_ids).order_by(
            'customer__title').order_by('order_id')

    def get_last_orders_comments(self, order_ids: list) -> QuerySet[Comments]:
        return Comments.objects.filter(order_id__in=order_ids).only(
            'order_id', 'created_at').order_by(
            'order_id', '-created_at'
        ).distinct('order_id')

    def has_orders_favorites(self, order_ids: list) -> List[bool]:
        favorites_count = Favorites.objects.filter(
            order_id__in=order_ids
        ).values('order_id').annotate(
            count=Count('id')
        )
        favorites_dict = {item['order_id']: item['count'] > 0 for item in
                          favorites_count}

        return [favorites_dict.get(order_id, False) for order_id in order_ids]

    def get_task_order_comments_num(self, order_ids: list) -> Dict[int, int]:
        task_comments_count = Comments.objects.filter(
            order_id__in=order_ids,
            is_task=1
        ).exclude(
            complete=1
        ).values('order_id').annotate(count=Count('id'))

        comments_dict = {item['order_id']: item['count'] for item in
                         task_comments_count}

        return comments_dict


class CostListRepo:
    def __init__(self, user_id: int):
        self.user_id = user_id

    def is_existing_search(self) -> bool:
        return Search.objects.filter(user_id=self.user_id).exists()

    def get_user_search(self) -> Search:
        return Search.objects.get(user_id=self.user_id)

    def get_search_costs(self, start: int, stop: int) -> QuerySet[Cost]:
        qs = Cost.objects.select_related('order').prefetch_related(
            'order__searchowners').filter(
            cost_filter_by_search(self.get_user_search())
        ).order_by('-created_at')

        if start and stop:
            return qs[(self.start - 1):self.stop]
        return qs

    def get_search_cost_approved_lists(self, start: int, stop: int) -> QuerySet[
        ApprovedList]:
        costs_ids = Cost.objects.filter(
            cost_filter_by_search(self.get_user_search())
        ).values_list('id', flat=True)

        if start and stop:
            costs_ids = costs_ids[(self.start - 1):self.stop]

        return ApprovedList.objects.filter(cost_id__in=costs_ids)
