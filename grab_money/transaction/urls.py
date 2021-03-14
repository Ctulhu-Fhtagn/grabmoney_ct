# Django:
from django.urls import path

# Localfolder:
from .views import (
    transaction_assign_category,
    transaction_create,
    transaction_delete,
    transaction_detail,
    transaction_edit,
    transaction_list,
    transaction_unknown_list,
)

app_name = "transaction"
urlpatterns = [
    path("", transaction_list, name="transaction-list"),
    path("unknown", transaction_unknown_list, name="transaction-unknown-list"),
    path(
        "assign-category/<int:id>",
        transaction_assign_category,
        name="transaction-assign-category",
    ),
    path("create/", transaction_create, name="transaction-create"),
    path("edit/<int:id>", transaction_edit, name="transaction-edit"),
    path(
        "edit/<int:id>/<int:category_id>",
        transaction_edit,
        name="transaction-edit-with-cat",
    ),
    path("delete/<int:id>", transaction_delete, name="transaction-delete"),
    path("detail/<int:id>", transaction_detail, name="transaction-detail"),
]
