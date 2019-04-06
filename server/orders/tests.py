from django.test import TestCase

from .models import Order
from markets.models import Market
from tickers.models import Ticker


class TestOrder(TestCase):

    def setUp(self) -> None:
        self.ticker1 = Ticker.objects.create(name="USD")
        self.ticker2 = Ticker.objects.create(name="EUR")
        self.market = Market.objects.create(name="USD/EUR",
                                            base_currency=self.ticker1,
                                            quote_currency=self.ticker2)

        for i in range(20):
            self.orders = Order.objects.create(market=self.market, )


    def test_market_exists(self):
        assert Market.objects.all().count() == 1
