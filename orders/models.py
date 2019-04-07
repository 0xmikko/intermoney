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
    market = models.ForeignKey(Market, blank=True, on_delete=models.CASCADE, null=True)
    order_type = models.IntegerField(default=ORDER_LIMIT)

    side = models.IntegerField(default=1)

    price = models.IntegerField(default=0)
    size = models.IntegerField(default=0)

    filled = models.IntegerField(default=0)
    status = models.IntegerField(default=0)

    hash_signature = models.CharField(max_length=1024, default='')

    created_at = models.DateTimeField(auto_now_add=True, editable=False, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=True, blank=True, null=True)

    def fill(self, filled : int):
        self.filled += filled
        if self.size > self.filled:
            self.status = Order.STATUS_PARTIALLY_FILLED
        else:
            self.status = Order.STATUS_FILLED
