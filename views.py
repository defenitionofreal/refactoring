from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from rest_framework.views import APIView
from rest_framework import serializers, response

from .serializers import *
from .services import *



class CountOrders(APIView):
    http_method_names = ["get"]

    def get(self, request):
        service = OrderListService(request.user.id)
        serializer = CountOrdersSerializer(
            service.count(
             request.query_params.get('start', 0),
             request.query_params.get('stop', 0)
            ), many=False
        )
        return response.Response(serializer.data)


class OrderList(LoginRequiredMixin, View):
    http_method_names = ["get"]

    def get(self, request):
        service = OrderListService(request.user.id)
        return render(
            request,
            'main/orders_list.html',
            service.context(
                request.query_params.get('start', 0),
                request.query_params.get('stop', 0)
            )
        )


class CountCosts(APIView):
    http_method_names = ["get"]

    def get(self, request):
        service = CostListService(request.user.id)
        serializer = CountCostsSerializer(
            service.count(
             request.query_params.get('start', 0),
             request.query_params.get('stop', 0)
            ), many=False
        )
        return response.Response(serializer.data)


class CostList(LoginRequiredMixin, View):
    http_method_names = ["get"]

    def get(self, request):
        service = CostListService(request.user.id)
        return render(
            request,
            'main/cost_list.html',
            service.context(
                request.query_params.get('start', 0),
                request.query_params.get('stop', 0)
            )
        )