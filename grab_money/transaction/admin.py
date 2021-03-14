# Django:
from django.contrib import admin

# Localfolder:
from .models import Transaction


# Register application 'Transaction' in admin-panel
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "account_from",
        "account_to",
        "category",
        "date",
        "amount",
        "description",
    )
    list_filter = ("date",)
