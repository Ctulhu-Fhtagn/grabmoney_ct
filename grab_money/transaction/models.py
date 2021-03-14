# Stdlib:
from datetime import datetime
from decimal import Decimal

# Django:
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.timezone import make_aware

# Firstparty:
from config.settings import base
from grab_money.bank_account.models import BalanceByDate, BankAccount
from grab_money.category.models import Category
from grab_money.currency.models import Currency
from grab_money.currency_rate.models import CurrencyRate
from grab_money.currency_rate.utils import get_currency_rate

DRAFT = "draft"
DONE = "done"
FAILED = "failed"
CANCEL = "cancel"

STATUS_CHOICES = [
    (DRAFT, "Draft"),
    (DONE, "Done"),
    (FAILED, "Failed"),
    (CANCEL, "Cancel"),
]


class Transaction(models.Model):
    owner = models.ForeignKey(
        base.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, default="2"
    )
    account_from = models.ForeignKey(
        BankAccount, on_delete=models.CASCADE, blank=False, related_name="account_from"
    )
    account_to = models.ForeignKey(
        BankAccount, on_delete=models.CASCADE, blank=False, related_name="account_to"
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False)
    date = models.DateTimeField(auto_now_add=False)
    amount = models.DecimalField(max_digits=20, decimal_places=6)
    description = models.TextField(blank=True)
    data = JSONField(default=dict)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=DRAFT)
    keyword = models.TextField(blank=True)

    def currency_exchange(currency_from, amount, date):
        if currency_from == "RUR":
            currency_from = "RUB"
        currency = Currency.objects.get(short_unit_label=currency_from)
        if CurrencyRate.objects.filter(currency_id=currency, date=date).exists():
            amount_exchange = (
                CurrencyRate.objects.filter(currency_id=currency, date=date)[0].rate
                * amount
            )
        else:
            rate = get_currency_rate(currency_from, date)

            new_rate = CurrencyRate()
            new_rate.currency_id = currency
            new_rate.rate = rate["rate"]
            new_rate.date = date
            new_rate.scale = rate["scale"]
            new_rate.save()

            amount_exchange = (
                CurrencyRate.objects.filter(currency_id=currency, date=date)[0].rate
                * amount
            )
        return amount_exchange

    def save(self, *args, **kwargs):
        unknown_category = Category.get_unknown_category()
        if self.status == DRAFT and self.category != unknown_category:
            self.status = DONE
        if not self.date:
            self.date = make_aware(datetime.now())
        self.save_balance_by_date()
        super().save(*args, **kwargs)

    def save_balance_by_date(self):
        self.amount = self.amount or 0.0
        account_from_balance = float(self.account_from.balance) - float(self.amount)
        account_to_balance = float(self.account_to.balance) + float(self.amount)

        bbd_1 = BalanceByDate.objects.filter(
            date=datetime.today(), account=self.account_from
        ).first()
        if not bbd_1:
            bbd_1 = BalanceByDate.objects.create(
                **{
                    "date": datetime.today(),
                    "owner": self.owner,
                    "account": self.account_from,
                    "balance": Decimal(0.0),
                }
            )
        bbd_2 = BalanceByDate.objects.filter(
            date=datetime.today(), account=self.account_to
        ).first()
        if not bbd_2:
            bbd_2 = BalanceByDate.objects.create(
                **{
                    "date": datetime.today(),
                    "owner": self.owner,
                    "account": self.account_to,
                    "balance": Decimal(0.0),
                }
            )
        if not bbd_1.balance:
            bbd_1.balance = account_from_balance
        else:
            bbd_1.balance = float(bbd_1.balance) - float(self.amount)
        bbd_1.save()
        if not bbd_2.balance:
            bbd_2.balance = account_to_balance
        else:
            bbd_2.balance = float(bbd_2.balance) + float(self.amount)
        bbd_2.save()

        self.account_from.balance = account_from_balance
        self.account_from.save_base()
        self.account_to.balance = account_to_balance
        self.account_to.save_base()

    @classmethod
    def reprocess_transactions(self, user):
        transactions = Transaction.objects.filter(
            owner=user, status=DRAFT, category=Category.objects.get(pk=1)
        )
        for transaction in transactions:
            category, category_account = Category.search_by_keyword(transaction.keyword)
            if category.id != 1:
                transaction.category = category
                transaction.account_to = category_account
                transaction.status = DONE
                transaction.save()

    def __str__(self):
        return str(self.amount)
