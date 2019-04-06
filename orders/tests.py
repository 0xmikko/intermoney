from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Order
from markets.models import Market
from tickers.models import Ticker


USER_MODEL = get_user_model()

class TestOrder(TestCase):

    def setUp(self) -> None:
        self.ticker1 = Ticker.objects.create(name="USD")
        self.ticker2 = Ticker.objects.create(name="EUR")
        self.market = Market.objects.create(name="USD/EUR",
                                            base_currency=self.ticker1,
                                            quote_currency=self.ticker2)

        self.Alice = USER_MODEL.objects.create_user(username="Alice", email="alice@yy.ru", password="hhhh")
        self.Bob = USER_MODEL.objects.create_user(username="Bob", email="bob@yy.ru", password="hhhh")

        # Creating Alice orders
        for i in range(20):
            Order.objects.create(sender=self.Alice,
                               side=Order.SIDES_SELL,
                               price=10000 + i*100,
                               size=100000+i*10000,
                               filled=0,
                               status=Order.STATUS_WAITING_NEW,
                               hash_signature="SIGA",
                               market=self.market)

        # Creating Alice orders
        for i in range(20):
            Order.objects.create(sender=self.Alice,
                               side=Order.SIDES_BUY,
                               price=10000 - i*100,
                               size=100000+i*10000,
                               filled=0,
                               status=Order.STATUS_WAITING_NEW,
                               hash_signature="SIGA",
                               market=self.market)

        # Creating Bob orders
        for i in range(20):
            Order.objects.create(sender=self.Bob,
                               side=Order.SIDES_BUY,
                               price=10000 - i*100,
                               size=100000+i*10000,
                               filled=0,
                               status=Order.STATUS_WAITING_NEW,
                               hash_signature="SIGA",
                               market=self.market)


    def test_market_exists(self):
        assert Market.objects.all().count() == 1

    def test_orders_created(self):
        assert Market.objects.all()[0].order_set.count() == 40
        print("---BID----")
        for order in Market.objects.all()[0].order_set.filter(side=Order.SIDES_BUY).order_by("-price"):
            print(order.price, order.size)

        print("---ASK----")
        for order in Market.objects.all()[0].order_set.filter(side=Order.SIDES_SELL).order_by("price"):
            print(order.price, order.size)
