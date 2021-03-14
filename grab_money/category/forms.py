# Django:
from django.forms import ModelForm
from django.urls import reverse

# Thirdparty:
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# Localfolder:
from .models import Category


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = [
            "category_name",
            "description",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "category_create"
        self.helper.form_class = "Category"
        self.helper.form_method = "post"
        self.helper.form_action = ""
        self.helper.add_input(Submit("submit", "Save"))


class EditCategoryForm(CategoryForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.id:
            self.helper.form_action = reverse(
                "category:category-edit", args=[self.instance.id]
            )
        else:
            self.helper.form_action = reverse("category-list")
        # self.helper.add_input(Submit("submit", "Save"))
        self.helper.inputs[0].value = "Save"
