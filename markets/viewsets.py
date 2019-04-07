import json

from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from orders.models import Order
from tickers.models import Ticker
from .models import Market
from .serializers import MarketSerializer


class MarketsViewSet(viewsets.ModelViewSet):
    """
    use /api/markets/create_market/ - to create bots
    use /api/markets/ - to list all markets
    """
    queryset = Market.objects.all()
    serializer_class = MarketSerializer

    @action(detail=False)
    def create_market(self, request):

        USER_MODEL = get_user_model()

        Market.objects.all().delete()
        Ticker.objects.all().delete()

        ticker1 = Ticker.objects.create(name="USD")
        ticker2 = Ticker.objects.create(name="EUR")

        market_usd_eur = Market.objects.create(name="USDEUR",
                                            base_currency=ticker1,
                                            quote_currency=ticker2)

        market_eur_usd = Market.objects.create(name="EURUSD",
                                            base_currency=ticker2,
                                            quote_currency=ticker1)

        names = ["Alice", "Bob", "Claudia", "Dodge", "Sapsan", "Eugene", "Eugene in Sapsan",
                 "Eugene in Sapsan writing DEX on Go"]

        bots = []

        for name in names:
            print(name)
            print(bots)
            queryset = USER_MODEL.objects.filter(username=name)
            if queryset.count() > 0:
                queryset.delete()
            pwd = name + "pwd"
            new_bot = USER_MODEL.objects.create_user(username=name, password=pwd)
            bots.append(new_bot)

        strategy_count = 3
        num =0

        for market in (market_eur_usd, market_usd_eur):
            for bot in bots:
                print("FFFF")
                print(bot)

                if num % strategy_count == 0:
                    for i in range(20):
                        Order.objects.create(sender=bot,
                                             side=Order.SIDES_SELL,
                                             price=10000 + i * 100,
                                             size=100000 + i * 10000,
                                             filled=0,
                                             status=Order.STATUS_WAITING_NEW,
                                             hash_signature="SIGA",
                                             market=market)

                if num % strategy_count == 1:
                    for i in range(20):
                        Order.objects.create(sender=bot,
                                             side=Order.SIDES_BUY,
                                             price=10000 - i * 100,
                                             size=100000 + i * 10000,
                                             filled=0,
                                             status=Order.STATUS_WAITING_NEW,
                                             hash_signature="SIGA",
                                             market=market)

                if num % strategy_count == 2:
                    for i in range(20):
                        Order.objects.create(sender=bot,
                                             side=Order.SIDES_BUY,
                                             price=0,
                                             size=100000 + i * 10000,
                                             filled=0,
                                             status=Order.STATUS_WAITING_NEW,
                                             hash_signature="SIGA",
                                             market=market)

                num += 1

        return Response("Bots were created", status=status.HTTP_200_OK)

    @action(detail=True)
    def process(self, request, pk):
        market_obj = get_object_or_404(Market, pk=pk)
        market_obj.process_queue()
        return Response("Matching cycle was done", status=status.HTTP_200_OK)


    @action(detail=True)
    def orderbook(self, request, pk):
        from orders.models import Order
        from .serializers import Level2Serializer
        market_obj = get_object_or_404(Market, pk=pk)
        market_obj.process_queue()
        market_obj.process_queue()
        market_obj.process_queue()
        asks = market_obj.get_level2(Order.SIDES_SELL)
        bids = market_obj.get_level2(Order.SIDES_BUY)


        print(asks)
        print(bids)
        asks_array = []
        bids_array = []
        for l in asks:
            price = str(l.get("price", 0))
            size = str(l.get("size", 0))
            asks_array.append([price, size])

        for l in bids:
            price = str(l.get("price", 0))
            size = str(l.get("size", 0))
            bids_array.append([price, size])

        l2 = {"ask": asks_array, "bid": bids_array}
        return Response(l2, status=status.HTTP_200_OK)





