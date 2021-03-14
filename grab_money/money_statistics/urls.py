# Django:
from django.urls import path

# Localfolder:
from .views import (
    account_credit,
    balance_by_date,
    credit_by_date,
    debit_credit_report,
    debit_credit_report_data,
    statistics,
    transaction_amount,
)

app_name = "money_statistics"
urlpatterns = [
    path("", statistics, name="statistics"),
    path(
        "transaction-amount-chart/", transaction_amount, name="transaction-amount-chart"
    ),
    path("credit-by-date/", credit_by_date, name="credit-by-date"),
    path("account-credit/<int:id>/", account_credit, name="account-credit"),
    path("balance-by-date/", balance_by_date, name="balance-by-date"),
    path("debit-credit-report/", debit_credit_report, name="debit-credit-report"),
    path(
        "debit-credit-report/data",
        debit_credit_report_data,
        name="debit-credit-report-data",
    ),
]
