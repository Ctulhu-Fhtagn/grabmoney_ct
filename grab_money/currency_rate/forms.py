# Django:
from django import forms
from django.contrib.auth.models import User
from django.urls import reverse

# Thirdparty:
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# Localfolder:
from .models import CurrencyRate


class CurrencyRateRefreshForm(forms.ModelForm):
    class Meta:
        model = CurrencyRate
        fields = ["date"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "currency-rate-refresh"
        self.helper.form_class = "CurrencyRate"
        self.helper.form_method = "post"
        self.helper.form_action = reverse("currency_rate:currency-rate-refresh")
        self.helper.add_input(Submit("submit", "Refresh"))
