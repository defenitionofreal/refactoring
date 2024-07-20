from django.db.models import Q

from prj.models import (
    Search, OrderResponsible, OrderComResponsible
)


def order_filter_by_search(search: Search) -> Q:
    filters = Q()

    if search.keyword:
        filters &= (
                Q(name__icontains=search.keyword) |
                Q(searchowners__icontains=search.keyword)
        )
    else:
        if search.is_goal:
            filters &= Q(is_goal=True)

        if search.is_favorite:
            filters &= Q(
                id__in=search.user.favorites_set.values_list('order__id',
                                                             flat=True))

        if search.manager:
            order_res_ids = list(OrderResponsible.objects.filter(
                user=search.manager
            ).values_list('order__id', flat=True))

            order_com_ids = list(OrderComResponsible.objects.filter(
                user=search.manager
            ).exclude(order__id__in=order_res_ids).values_list('order__id',
                                                               flat=True))

            filters &= Q(id__in=list(set(order_res_ids + order_com_ids)))

        if search.stage:
            filters &= Q(stage=search.stage)

        if search.company:
            filters &= Q(cityid=search.company)

        if search.customer:
            filters &= Q(searchowners=search.customer)

    return filters


def cost_filter_by_search(search: Search) -> Q:
    filters = Q()

    if search.keyword:
        filters &= (
                Q(description__icontains=search.keyword) |
                Q(section__icontains=search.keyword) |
                Q(orderid__name__icontains=search.keyword)
        )
        return filters

    if search.is_goal:
        filters &= Q(order__is_goal=True)

    if search.is_favorite:
        filters &= Q(
            order_id__in=search.user.favorites_set.values_list('order__id',
                                                               flat=True))

    if search.manager:
        filters &= Q(user=search.manager)

    if search.stage:
        filters &= Q(order__stage=search.stage)

    if search.company:
        filters &= Q(order__cityid=search.company)

    if search.customer:
        filters &= Q(order__searchowners=search.customer)

    return filters
