# Django:
from django.contrib import admin

# Localfolder:
from .models import Currency


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = (
        "full_unit_label",
        "subunit_label",
        "short_unit_label",
        "symbol",
        "rounding",
    )
    list_filter = ("full_unit_label", "short_unit_label")
    search_fields = ("short_unit_label",)
