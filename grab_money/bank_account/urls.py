# Django:
from django.urls import path

# Localfolder:
from . import views

app_name = "bank_account"
urlpatterns = [
    path("", views.account_name_list, name="account-list"),
    path("create/", views.account_name_create, name="add-new-bank_account"),
    path("save/", views.account_name_list),
    path("delete/<int:id>/", views.account_name_delete, name="account-delete"),
    path("edit/<int:id>/", views.account_name_edit, name="bank-account-edit"),
    path("detail/<int:id>/", views.account_detail, name="account-detail"),
]
