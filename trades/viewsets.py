from rest_framework import viewsets

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

