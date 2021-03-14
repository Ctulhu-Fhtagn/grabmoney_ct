# Django:
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TransactionConfig(AppConfig):
    name = "grab_money.transaction"
    verbose_name = _("Transaction")
