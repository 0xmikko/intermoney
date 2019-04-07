from django.db import models
from tickers.models import Ticker


class Market(models.Model):
    """
    Market is an entity which 
    """
    name = models.CharField(max_length=30, default='', unique=True)
    smart_contract_address = models.CharField(max_length=42, default=('0x0'))
    base_currency = models.ForeignKey(Ticker, blank=True, on_delete=models.CASCADE, null=True, related_name='base_market')
    quote_currency = models.ForeignKey(Ticker, blank=True, on_delete=models.CASCADE, null=True, related_name='quote_market')

    @property
    def last_price(self):
        from trades.models import Trade
        last_trade = Trade.objects.filter(status=Trade.STATUS_OK).order_by("-created_at").last()
        return last_trade.price if last_trade != None else 0

    @property
    def max_24_price(self):
        return 0

    @property
    def min_24_price(self):
        return 0

    @property
    def volume_24(self):
        return 0

    @property
    def change_24(self):
        return 0

    @classmethod
    def get_market_by_tickers(cls, name):
        """
        Return market by name
        :param name:
        :return:
        """
        objs = Market.objects.filter(name=name)
        if objs.count() != 1:
            raise Market.DoesNotExist

        return objs[0]

    def process_queue(self):
        from orders.models import Order
        queue = self.order_set.filter(status=Order.STATUS_WAITING_NEW).order_by("created_at")
        for order in queue:
            order.process()


    def _get_bid_ask(self):
        """

        :return: tuple with bid and ask price
        """
        from orders.models import Order
        bid = self.order_set.filter(side=Order.SIDES_BUY,
                                    status__in=[Order.STATUS_NEW, Order.STATUS_UPDATED, Order.STATUS_PARTIALLUY_FILLED])\
                  .exclude(price=0)\
                  .order_by("-price")

        ask = self.order_set.filter(side=Order.SIDES_SELL,
                                    status__in=[Order.STATUS_NEW, Order.STATUS_UPDATED, Order.STATUS_PARTIALLUY_FILLED])\
                  .exclude(price=0)\
                  .order_by("price")

        bid_price = None
        ask_price = None

        if len(bid) > 0:
            bid_price = bid[0].price
        if len(ask) > 0:
            ask_price = ask[0].price

        return (bid_price, ask_price)

    def __str__(self):
        return self.name


