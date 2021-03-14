# Django:
from django import apps
from django.db import models

# Firstparty:
from config.settings import base
from grab_money.currency.models import Currency


class Category(models.Model):

    # Default info for each category
    category_name = models.CharField(max_length=25, blank=False)
    description = models.TextField(blank=True)
    is_default = models.BooleanField(default=True, blank=False)
    # If category is default(is_default = True)
    mcc_code = models.CharField(max_length=25, blank=True)
    # If category is personalized (is_default = False)
    owner = models.ForeignKey(
        base.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True
    )

    def __str__(self):
        return self.category_name

    def save(self, *args, **kwargs):
        # TODO: Auto Create new Bank Account for Category
        super().save(*args, **kwargs)

    @classmethod
    def get_unknown_category(cls):
        return cls.objects.get(pk=1)

    @classmethod
    def search_by_keyword(cls, word):
        User = apps.apps.get_model(base.AUTH_USER_MODEL)
        BankAccount = apps.apps.get_model("bank_account.BankAccount")
        keywords = CategoryKeyword.objects.filter(word=word)
        if len(keywords):
            category = keywords.first().category
            account, account_created = BankAccount.objects.get_or_create(
                owner=User.objects.get(pk=1),
                name=category.category_name,
                type="Debit",
                opening_debit=0,
                opening_credit=0,
                currency=Currency.objects.get(short_unit_label="BYN"),
            )
            if account_created:
                account.save()
            return category, account
        return Category.objects.get(pk=1), BankAccount.objects.get(pk=1)


class CategoryKeyword(models.Model):

    word = models.CharField(max_length=100, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True)
