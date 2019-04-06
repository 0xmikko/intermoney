from django.db import models
from markets.models import Market


class Order(models.Model):

    SIDE_BUY = 1
    SIDE_SELL = -1

    STATUS_UNKNOWN = 0

    sender = models.CharField(max_length=42, default=('0x0'))
    side = models.IntegerField(default=1)

    size = models.DecimalField(decimal_places=2, default=0, max_digits=10)
    filled = models.DecimalField(decimal_places=2, default=0, max_digits=10)
    status = models.IntegerField(default=0)
    market = models.ForeignKey(Market, blank=True, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=True, blank=True, null=True)

