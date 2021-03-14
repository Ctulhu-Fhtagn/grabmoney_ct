# Django:
from django.urls import path

# Localfolder:
from .views import (
    category_create,
    category_delete,
    category_detail,
    category_edit,
    category_list,
)

app_name = "category"
urlpatterns = [
    path("", category_list, name="category-list"),
    path("create/", category_create, name="category-create"),
    path("edit/<int:id>/", category_edit, name="category-edit"),
    path("delete/<int:id>/", category_delete, name="category-delete"),
    path("detail/<int:id>/", category_detail, name="category-detail"),
]
