from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer


class OrdersViewSet(viewsets.ViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer