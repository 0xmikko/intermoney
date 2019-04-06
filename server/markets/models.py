from django.db import models
from tickers.models import Ticker


class Market(models.Model):
    name = models.CharField(max_length=30, default='')
    smart_contract_address = models.CharField(max_length=42, default=('0x0'))
    base_currency = models.ForeignKey(Ticker, blank=True, on_delete=models.CASCADE, null=True, related_name='base_market')
    quote_currency = models.ForeignKey(Ticker, blank=True, on_delete=models.CASCADE, null=True, related_name='quote_market')



