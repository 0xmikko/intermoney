from django.db import models


class Ticker(models.Model):
    name = models.CharField(max_length=30, default='')
    smart_contract_address = models.CharField(max_length=42, default=('0x0'))