# Django:
from django.db import models

# Firstparty:
from config.settings import base
from grab_money.currency import models as currency_model
from grab_money.transaction import models as transaction


class BankAccount(models.Model):

    owner = models.ForeignKey(
        base.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False
    )
    name = models.CharField(max_length=150)
    number_account = models.CharField(max_length=35, blank=True)
    number_card = models.CharField(max_length=35, blank=True)
    currency = models.ForeignKey(currency_model.Currency, on_delete=models.CASCADE)
    TYPE_CHOICES = [("Debit", "Debit"), ("Credit", "Credit")]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    balance = models.DecimalField(
        max_digits=19, decimal_places=2, blank=True, null=True
    )
    opening_debit = models.DecimalField(
        max_digits=19, decimal_places=2, blank=True, null=True
    )
    opening_credit = models.DecimalField(
        max_digits=19, decimal_places=2, blank=True, null=True
    )
    CATEGORY_CHOICES = [
        ("Cash", "Cash"),
        ("Bank", "Bank"),
        ("Card", "Card"),
        ("Monybox", "Monybox"),
        ("Deposit", "Deposit"),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def save(self, *args, **kwargs):
        self.balance = self.opening_debit - self.opening_credit
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.balance} {self.currency.short_unit_label})"


class BalanceByDate(models.Model):
    owner = models.ForeignKey(
        base.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    date = models.DateField()
    balance = models.DecimalField(
        max_digits=19, decimal_places=2, blank=True, null=True
    )
