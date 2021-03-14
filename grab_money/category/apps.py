# Django:
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CategoryConfig(AppConfig):
    name = "grab_money.category"
    verbose_name = _("Category")
