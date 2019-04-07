from django.db import models
from django.conf import settings
from markets.models import Market


class Order(models.Model):
    """

    """

    SIDES_BUY = 1
    SIDES_SELL = 0

    SIDES_CHOICES = (
        (SIDES_BUY, 'BUY'),
        (SIDES_SELL, 'SELL'),
    )

    STATUS_UNKNOWN = 0
    STATUS_WAITING_NEW = 1
    STATUS_NEW = 2
    STATUS_REJECTED = 4
    STATUS_WAITING_CANCELLED = 5
    STATUS_CANCELLED = 6
    STATUS_PARTIALLY_FILLED = 7
    STATUS_FILLED = 8
    STATUS_WAITING_UPDATE = 9
    STATUS_UPDATED = 10

    STATUSES = (
        (STATUS_UNKNOWN, "Unknown"),
        (STATUS_WAITING_NEW, "Waiting New"),
        (STATUS_NEW, "Status New"),
        (STATUS_REJECTED, "Rejected"),
        (STATUS_WAITING_CANCELLED, "Waiting Cancel"),
        (STATUS_CANCELLED, "Cancelled"),
        (STATUS_PARTIALLY_FILLED, "Partially Filled"),
        (STATUS_FILLED, "Filled"),
        (STATUS_WAITING_UPDATE, "Waiting Update"),
        (STATUS_UPDATED, "Updated"),
    )

    ORDER_LIMIT = 0
    ORDER_MARKET = 1

    ORDERS_TYPES = (
        (ORDER_LIMIT, "Limit"),
        (ORDER_MARKET, "Market"),
    )

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True )
    market = models.ForeignKey(Market, blank=True, on_delete=models.CASCADE, null=True, related_name='order_set')
    order_type = models.IntegerField(default=ORDER_LIMIT, choices=ORDERS_TYPES)

    side = models.IntegerField(default=1, choices=SIDES_CHOICES)

    price = models.DecimalField(default=0, max_digits=40, decimal_places=0)
    size = models.DecimalField(default=0, max_digits=40, decimal_places=0)

    filled = models.DecimalField(default=0, max_digits=40, decimal_places=0)
    status = models.IntegerField(default=0, choices=STATUSES)

    hash_signature = models.CharField(max_length=1024, default='')

    created_at = models.DateTimeField(auto_now_add=True, editable=False, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=True, blank=True, null=True)

    def __str__(self):
        return str(self.sender) + " " + str(self.get_order_type_display()) + " " + str(self.get_status_display()) + " " + str(self.price)

    def fill(self, filled : int):
        self.filled += filled
        if self.size > self.filled:
            self.status = Order.STATUS_PARTIALLY_FILLED
        else:
            self.status = Order.STATUS_FILLED

    def process(self):
        if self.status == self.STATUS_WAITING_NEW:
            self.status = self.STATUS_NEW
            self.save()

        #            best_bid_price, best_ask_price = self.get_bid_ask(self.market)
        if self.price == 0:
            self.take()
            self.status = self.STATUS_FILLED
            self.save()
        if self.price != 0:
            self.take()

    def take(self):
        from trades.models import Trade
        depth = []
        if self.side == self.SIDES_SELL:
            depth = self.market.order_set.filter(side=self.SIDES_BUY,
                                                 status__in=[self.STATUS_NEW, self.STATUS_UPDATED, self.STATUS_PARTIALLY_FILLED])\
                        .exclude(price=0).order_by("-price")

        if self.side == self.SIDES_BUY:
            depth = self.market.order_set.filter(side=self.SIDES_SELL,
                                                 status__in=[self.STATUS_NEW, self.STATUS_UPDATED, self.STATUS_PARTIALLY_FILLED])\
                                         .exclude(price=0).order_by("price")

        for o in depth:
            if (self.side == self.SIDES_SELL and self.price != 0 and self.price > o.price) or (self.side == self.SIDES_BUY and self.price != 0 and self.price < o.price):
                break

            if self.size - self.filled > o.size - o.filled:
                fill_size = o.size - o.filled
            else:
                fill_size = self.size - self.filled

            o.fill(fill_size)
            self.fill(fill_size)
            o.save()
            self.save()

            if self.side == self.SIDES_SELL:
                self_buy = o
                self_sell = self
            else:
                self_buy = self
                self_sell = o

            Trade.objects.create(order_buy=self_buy, order_sell=self_sell, price=o.price, side=self.side,
                                 size=fill_size)

            if self.status == self.STATUS_FILLED:
                break