from enum import Enum

from django.db import models
from django.conf import settings
from markets.models import Market


class Order(models.Model):
    """

    """

    class Sides(Enum):
        BUY = 1
        SELL = 0

    SIDES = (
        (Sides.BUY, 'BUY'),
        (Sides.SELL, 'SELL'),
    )

    class OrderStatuses(Enum):
        Unknown = 0
        WaitingNew = 1
        StatusNew = 2
        Rejected = 4
        WaitingCancel = 5
        Canceled = 6
        PartiallyFilled = 7
        Filled = 8
        WaitingUpdate = 9
        Updated = 10

    STATUSES = (
        (OrderStatuses.Unknown, "Unknown"),
        (OrderStatuses.WaitingNew, "Waiting New"),
        (OrderStatuses.StatusNew, "Status New"),
        (OrderStatuses.Rejected, "Rejected"),
        (OrderStatuses.WaitingCancel, "Waiting Cancel"),
        (OrderStatuses.Canceled, "Cancelled"),
        (OrderStatuses.PartiallyFilled, "Partially Filled"),
        (OrderStatuses.Filled, "Filled"),
        (OrderStatuses.WaitingUpdate, "Waiting Update"),
        (OrderStatuses.Updated, "Updated")
    )

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True )

    side = models.IntegerField(default=1, choices=SIDES)

    price = models.IntegerField(default=0)
    size = models.IntegerField(default=0)

    filled = models.IntegerField(default=0)
    status = models.IntegerField(default=0, choices=STATUSES)

    hash_signature = models.CharField(max_length=1024, default='')

    market = models.ForeignKey(Market, blank=True, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, editable=True, blank=True, null=True)

