# Django:
from django.db import models
from django.urls import reverse


class Currency(models.Model):
    # full name (ex. Dollar, Euro etc.)
    full_unit_label = models.CharField(max_length=15)

    # lesser unit (ex. Cents, Kopeikas)
    subunit_label = models.CharField(max_length=15)

    # short international name (USD, BYN, EUR)
    short_unit_label = models.CharField(max_length=4, blank=False)

    # one char symbol (ex. $)
    symbol = models.CharField(max_length=4, blank=True)

    # minimal value
    rounding = models.FloatField()

    def __str__(self):
        return self.short_unit_label
