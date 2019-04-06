from django.conf import settings
from django.db import models
from .tasks import update_balances


class BalanceManager(models.Manager):
    """

    """

    def update_balances(self):
        pass


class Balance(models.Model):
    """
    Sync balances from Ethereum
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    balance = models.IntegerField(default=0)


