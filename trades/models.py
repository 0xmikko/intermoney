from django.db import models
from orders.models import Order


class Trade(models.Model):

    # ToDo: export constants into another entity
    SIDES_BUY = 1
    SIDES_SELL = 0

    SIDES_CHOICES = (
        (SIDES_BUY, 'BUY'),
        (SIDES_SELL, 'SELL'),
    )

    order_buy = models.ForeignKey(Order, related_name="trade_buy", on_delete=models.CASCADE)
    order_sell = models.ForeignKey(Order, related_name="trade_sell", on_delete=models.CASCADE)
    price = models.IntegerField(default=0)
    side = models.IntegerField(default=0, choices=SIDES_CHOICES)
