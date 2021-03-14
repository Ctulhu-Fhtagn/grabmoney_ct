# Django:
from django.contrib import admin

# Localfolder:
from .models import BalanceByDate, BankAccount


@admin.register(BankAccount)
class AccountAdmin(admin.ModelAdmin):
    list_display = ["name", "number_account", "number_card", "currency"]
    exclude = ["balance"]


@admin.register(BalanceByDate)
class BalanceByDateAdmin(admin.ModelAdmin):
    list_display = ["owner", "account", "date", "balance"]
