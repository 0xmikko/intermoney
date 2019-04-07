from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Trade
from .serializers import TradesSerializer


class TradesViewSet(viewsets.ModelViewSet):
    """
    Orders API
    GET /api/orders/orderbook - returns orderbook
    GET /api/orders/active - return active user orders
    GET /api/orders/history - return history of user orders
    POST /api/orders/buy_market
    """
    queryset = Trade.objects.all()
    serializer_class = TradesSerializer

    @action(detail=False)
    def to_eth(self, request):
        Trade.send_trades()
        return Response("Trades were sent to blockchain", status=200)
