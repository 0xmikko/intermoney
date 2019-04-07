from django.db import models
from orders.models import Order


class Trade(models.Model):

    # ToDo: export constants into another entity
    SIDES_BUY = 1
    SIDES_SELL = 0

    STATUS_NEW = 0
    STATUS_PROCESSING = 1
    STATUS_OK = 2
    STATUS_REJECTED = 3

    SIDES_CHOICES = (
        (SIDES_BUY, 'BUY'),
        (SIDES_SELL, 'SELL'),
    )

    STATUS_CHOICES = (
        (STATUS_NEW, 'NEW'),
        (STATUS_PROCESSING, 'PROCESSING'),
        (STATUS_OK, 'OK'),
        (STATUS_REJECTED, 'REJECTED')
    )

    order_buy = models.ForeignKey(Order, related_name="trade_buy", on_delete=models.CASCADE)
    order_sell = models.ForeignKey(Order, related_name="trade_sell", on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    size = models.IntegerField(default=0)
    side = models.IntegerField(default=0, choices=SIDES_CHOICES)
    status = models.IntegerField(default=STATUS_NEW, choices=STATUS_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True, editable=False, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=True, blank=True, null=True)
