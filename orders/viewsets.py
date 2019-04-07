from rest_framework import viewsets
from rest_framework.decorators import action

from .models import Order
from .serializers import OrderSerializer


class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False)
    def orderbook(self, request):
        market_name = request.GET.get("market")
        pass

    @action(detail=False)
    def active(self, request):
        # Paginator
        page = request.GET.get("page")
        size = request.GET.get("size")
        type = request.GET.get("type")

    @action(detail=False)
    def history(self, request):
        # List last orders
        pass

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