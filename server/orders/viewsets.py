from rest_framework import viewsets
from rest_framework.decorators import action

from .models import Order
from .serializers import OrderSerializer


class OrdersViewSet(viewsets.ViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False, methods=['POST'])
    def buy_market(self, request):
        pass

    @action(detail=False, methods=['POST'])
    def sell_market(self, request):
        pass

    @action(detail=False, methods=['POST'])
    def buy_limit(self, request):
        pass

    @action(detail=False, methods=['POST'])
    def sell_limit(self, request):
        pass