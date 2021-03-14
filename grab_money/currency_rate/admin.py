# Django:
from django.contrib import admin

# Localfolder:
from .models import CurrencyRate


@admin.register(CurrencyRate)
class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "currency_id",
        "rate",
        "date",
    )
    list_filter = (
        "name",
        "date",
    )
    search_fields = (
        "name",
        "date",
    )
