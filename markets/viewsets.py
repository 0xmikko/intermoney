from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from orders.models import Order
from tickers.models import Ticker
from .models import Market
from .serializers import MarketSerializer


class MarketsViewSet(viewsets.ModelViewSet):
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
            USER_MODEL.objects.get(username=name).delete()
            new_bot_email = name + "@inmtermoney.com"
            pwd = name + "pwd"
            new_bot = USER_MODEL.objects.create_user(username=name, email=new_bot_email, password=pwd)
            bots.append(new_bot)

        strategy_count = 3
        for num, bot in enumerate(bots):

            if num % strategy_count == 0:
                for i in range(20):
                    Order.objects.create(sender=bot,
                                         side=Order.SIDES_SELL,
                                         price=10000 + i * 100,
                                         size=100000 + i * 10000,
                                         filled=0,
                                         status=Order.STATUS_WAITING_NEW,
                                         hash_signature="SIGA",
                                         market=market_usd_eur)

            if num % strategy_count == 1:
                for i in range(20):
                    Order.objects.create(sender=bot,
                                         side=Order.SIDES_BUY,
                                         price=10000 - i * 100,
                                         size=100000 + i * 10000,
                                         filled=0,
                                         status=Order.STATUS_WAITING_NEW,
                                         hash_signature="SIGA",
                                         market=market_usd_eur)

            if num % strategy_count == 2:
                for i in range(2):
                    Order.objects.create(sender=bot,
                                         side=Order.SIDES_BUY,
                                         price=0,
                                         size=100000 + i * 10000,
                                         filled=0,
                                         status=Order.STATUS_WAITING_NEW,
                                         hash_signature="SIGA",
                                         market=market_usd_eur)

            return Response("Bots were created", status=status.HTTP_200_OK)





