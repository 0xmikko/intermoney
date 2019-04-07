from django.db import models
from tickers.models import Ticker


class Market(models.Model):
    """
    Market is an entity which 
    """
    name = models.CharField(max_length=30, default='')
    smart_contract_address = models.CharField(max_length=42, default=('0x0'))
    base_currency = models.ForeignKey(Ticker, blank=True, on_delete=models.CASCADE, null=True, related_name='base_market')
    quote_currency = models.ForeignKey(Ticker, blank=True, on_delete=models.CASCADE, null=True, related_name='quote_market')

    @property
    def last_price(self):
        pass

    @property
    def max_24_price(self):
        pass

    @property
    def min_24_price(self):
        pass

    @property
    def volume_24(self):
        pass

    @property
    def change_24(self):
        pass

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


