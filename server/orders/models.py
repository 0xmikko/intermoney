from django.db import models
from django.conf import settings
from markets.models import Market


class Order(models.Model):

    SIDE_BUY = 1
    SIDE_SELL = -1

    STATUS_UNKNOWN = 0

    sender =models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True )
    side = models.IntegerField(default=1)

    price = models.IntegerField(default=0)
    size = models.IntegerField(default=0)

    filled = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    hash_signature = models.CharField(max_length=1024, default='')
    market = models.ForeignKey(Market, blank=True, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=True, blank=True, null=True)

