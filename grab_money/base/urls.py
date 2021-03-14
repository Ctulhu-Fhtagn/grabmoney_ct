# Django:
from django.urls import path

# Localfolder:
from . import views

app_name = "base"
urlpatterns = [
    path(
        "upload-transaction-file/",
        views.upload_transaction_file,
        name="upload-transaction-file",
    ),
]
