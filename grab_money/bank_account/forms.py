# Django:
from django import forms
from django.forms import ModelForm
from django.urls import reverse

# Thirdparty:
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# Firstparty:
from grab_money.bank_account.models import BankAccount


# Create the form class.
class BankAccountForm(ModelForm):
    class Meta:
        model = BankAccount
        fields = [
            "name",
            "number_account",
            "number_card",
            "currency",
            "opening_debit",
            "opening_credit",
            "category",
            "type",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "add-new-bank_account"
        self.helper.form_class = "NewBankAccount"
        self.helper.form_method = "post"
        self.helper.form_action = ""
        self.helper.add_input(Submit("submit", "create"))


class EditBankAccountForm(BankAccountForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_action = reverse(
            "bank_account:bank-account-edit", args=[self.instance.id]
        )
        self.helper.inputs[0].value = "save"
