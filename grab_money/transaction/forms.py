# Django:
from django.forms import Form, ModelChoiceField, ModelForm
from django.urls import reverse

# Thirdparty:
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# Firstparty:
from grab_money.category.models import Category

# Localfolder:
from .models import Transaction


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = [
            "account_from",
            "account_to",
            "category",
            "amount",
            "description",
            "date",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "transaction_create"
        self.helper.form_class = "NewTransaction"
        self.helper.form_method = "post"
        self.helper.form_action = ""
        self.helper.add_input(Submit("submit", "Save"))


class EditTransactionForm(TransactionForm):
    def __init__(self, *args, **kwargs):
        category_id = kwargs.get("category_id")
        if "category_id" in kwargs:
            del kwargs["category_id"]
        super().__init__(*args, **kwargs)
        if category_id:
            self.helper.form_action = reverse(
                "transaction:transaction-edit-with-cat",
                args=[self.instance.id, category_id],
            )
        else:
            self.helper.form_action = reverse(
                "transaction:transaction-edit", args=[self.instance.id],
            )
        self.helper.inputs[0].value = "Save"


class AssignCategoryTransactionForm(Form):
    category = ModelChoiceField(queryset=Category.objects.all())
