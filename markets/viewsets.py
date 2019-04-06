from rest_framework import viewsets
from .models import Market
from .serializers import MarketSerializer


class MarketsViewSet(viewsets.ModelViewSet):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer

