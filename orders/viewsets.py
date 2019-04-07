from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from markets.models import Market
from .models import Order
from .serializers import OrderSerializer


USER_MODEL = get_user_model()

class OrdersViewSet(viewsets.ModelViewSet):
    """
    Orders API
    GET /api/orders/orderbook - returns orderbook
    GET /api/orders/active - return active user orders
    GET /api/orders/history - return history of user orders
    POST /api/orders/buy_market
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False)
    def orderbook(self, request):
        market_name = request.GET.get("market")

        try:
            market = Market.get_market_by_tickers(market_name)
            return Response("It works", status=status.HTTP_200_OK)

        except Market.DoesNotExist:
            return Response("Market not found", status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def active(self, request):

        print(request.user)
        if request.user.is_anonymous():
            return Response("Authentication error", status=status.HTTP_400_BAD_REQUEST)

        user = USER_MODEL(pk=request.user)
        print(user)
        # Paginator
        page = request.GET.get("page")
        size = request.GET.get("size")
        type = request.GET.get("type")

        queryset = Order.objects.filter(status=Order.STATUS_WAITING_NEW, sender=user)

    @action(detail=False)
    def history(self, request):
        # Add user checking
        queryset = Order.objects.all()[:10]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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