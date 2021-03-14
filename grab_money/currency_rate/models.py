# Django:
from django.db import models

# Firstparty:
from grab_money.currency.models import Currency


class CurrencyRate(models.Model):
    name = models.CharField(max_length=150)
    currency_id = models.ForeignKey(Currency, on_delete=models.CASCADE)
    rate = models.FloatField()
    date = models.DateField()
    scale = models.CharField(max_length=10, default=1)
