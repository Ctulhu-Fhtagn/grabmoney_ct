# Django:
from django.urls import path

# Localfolder:
from .views import currency_rate_detail, currency_rate_list, currency_rate_refresh

app_name = "currency_rate"
urlpatterns = [
    path("<str:date>", currency_rate_list, name="currency-rate-list"),
    path("refresh/", currency_rate_refresh, name="currency-rate-refresh"),
    path("<str:shortalias>/", currency_rate_detail, name="currency-rate-detail"),
]
