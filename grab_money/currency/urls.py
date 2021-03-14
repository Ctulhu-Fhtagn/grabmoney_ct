# Django:
from django.urls import path

# Localfolder:
from .views import currency_list

app_name = "currency"
urlpatterns = [path("", currency_list, name="currency-list")]
