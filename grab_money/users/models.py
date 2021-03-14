# Django:
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, IntegerField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    # name = CharField(max_length = 128, blank = True)
    # age = IntegerField(blank = False, default = 18)

    # LANGUAGE_CHOICES = (
    #     ('ru', 'Русский'),
    #     ('en', 'English')
    # )
    # language = CharField(max_length = 2, blank = False, choices = LANGUAGE_CHOICES, default = 'en')

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
