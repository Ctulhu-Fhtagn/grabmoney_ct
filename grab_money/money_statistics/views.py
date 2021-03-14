# Django:
# Stdlib:
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

# Thirdparty:
import pandas as pd

# Firstparty:
from grab_money.bank_account.models import BalanceByDate, BankAccount
from grab_money.transaction.models import DONE, Transaction


@login_required(login_url="/accounts/login/")
def statistics(request):
    context = {}
    return render(request, "money_statistics/list.html", context)


@login_required(login_url="/accounts/login/")
def transaction_amount(request):
    labels = []
    data = []
    amounts = Transaction.objects.all().order_by("-date")[:9]
    for entry in amounts:
        labels.append(entry.date)
        data.append(entry.amount)

    return JsonResponse(data={"labels": labels, "data": data,})


def credit_by_date(request):
    labels = []
    data = []

    # Forming queryset of transactions
    queryset = Transaction.objects.filter(owner=request.user).order_by("date")

    # Creating list of 'date - amount' of transactions
    date = []

    for transaction in queryset:
        if transaction.date not in date:
            date.append([transaction.date, 0])
    for transaction in queryset:
        for date_debit in date:
            if date_debit[0] == transaction.date:
                date_debit[1] += transaction.amount

    for date_debit in date:
        date_debit[0] = date_debit[0].date()

    # Forming unique dates in labels and summing amounts in data
    for date_debit in date:
        if date_debit[0] in labels:
            data[labels.index(date_debit[0])] += date_debit[1]
        else:
            labels.append(date_debit[0])
            data.append(date_debit[1])

    # Data will be shown from '0' amount
    data.append(0)

    return JsonResponse(data={"labels": labels, "data": data,})


def credit_by_date(request):
    labels = []
    data = []

    queryset = Transaction.objects.filter(owner=request.user).order_by("date")

    # Creating list of 'date - amount' of transactions
    date = []

    for transaction in queryset:
        if transaction.date not in date:
            date.append([transaction.date, 0])
    for transaction in queryset:
        for date_credit in date:
            if date_credit[0] == transaction.date:
                date_credit[1] += transaction.amount

    for date_credit in date:
        date_credit[0] = date_credit[0].date()

    # Forming unique dates in labels and summing amounts in data
    for date_credit in date:
        if date_credit[0] in labels:
            data[labels.index(date_credit[0])] += date_credit[1]
        else:
            labels.append(date_credit[0])
            data.append(date_credit[1])

    # Data will be shown from '0' amount
    data.append(0)

    return JsonResponse(data={"labels": labels, "data": data,})


@login_required(login_url="/accounts/login/")
def balance_by_date(request):
    labels = []
    data = []
    queryset = BalanceByDate.objects.filter(owner=request.user).order_by("date")
    for entry in queryset:
        labels.append(entry.date)
        data.append(entry.balance)

    # Data will be shown from '0' amount
    data.append(0)

    return JsonResponse(data={"labels": labels, "data": data,})


@login_required(login_url="/accounts/login/")
def account_credit(request, id):
    labels = []
    data = []

    # Forming queryset of transactions
    queryset = Transaction.objects.filter(
        owner=request.user, account_from=BankAccount.objects.get(pk=id)
    ).order_by("date")

    # Creating list of 'date - amount' of transactions
    date = []

    for transaction in queryset:
        if transaction.date not in date:
            date.append([transaction.date, 0])
    for transaction in queryset:
        for date_debit in date:
            if date_debit[0] == transaction.date:
                date_debit[1] += transaction.amount

    for date_debit in date:
        date_debit[0] = date_debit[0].date()

    # Forming unique dates in labels and summing amounts in data
    for date_debit in date:
        if date_debit[0] in labels:
            data[labels.index(date_debit[0])] += date_debit[1]
        else:
            labels.append(date_debit[0])
            data.append(date_debit[1])

    # Data will be shown from '0' amount
    data.append(0)

    return JsonResponse(data={"labels": labels, "data": data,})


@login_required(login_url="/accounts/login/")
def debit_credit_report(request):
    context = {}
    return render(request, "money_statistics/debit_credit_report.html", context)


def get_average(transactions):
    columns = list("xy")

    data = []
    for row in transactions:
        data += [[row.date.date(), float(row.amount)]]
    data = pd.DataFrame(data=data, columns=columns)
    result = data.sort_values("x").groupby("x").sum().mean()
    return float(result)


@login_required(login_url="/accounts/login/")
def debit_credit_report_data(request):
    default_filters = dict(status=DONE, owner=request.user,)
    user_accounts = BankAccount.objects.filter(owner=request.user)
    user_accounts_ids = [x.id for x in user_accounts]
    all_transactions = Transaction.objects.filter(**default_filters).order_by("date")
    credit_transactions = Transaction.objects.filter(
        **default_filters, account_from__in=user_accounts_ids
    )
    debit_transactions = Transaction.objects.filter(
        **default_filters, account_to__in=user_accounts_ids
    )

    start_date = all_transactions.first().date.date().strftime("%Y-%m-%d")
    end_date = all_transactions.last().date.date().strftime("%Y-%m-%d")

    labels = [x.date() for x in pd.date_range(start_date, end_date)]

    credit_data = {}
    for row in credit_transactions:
        if row.date.date() not in credit_data:
            credit_data[row.date.date()] = -float(row.amount)
        else:
            credit_data[row.date.date()] -= float(row.amount)

    debit_data = {}
    for row in debit_transactions:
        if row.date.date() not in debit_data:
            debit_data[row.date.date()] = float(row.amount)
        else:
            debit_data[row.date.date()] += float(row.amount)

    all_data = {}
    for date_key in sorted(
        set([x for x in credit_data.keys()] + [x for x in debit_data.keys()])
    ):
        all_data[date_key] = credit_data.get(date_key, 0.0) + debit_data.get(
            date_key, 0.0
        )

    credit_data = [{"x": x, "y": y} for x, y in credit_data.items()]
    debit_data = [{"x": x, "y": y} for x, y in debit_data.items()]
    all_data = [{"x": x, "y": y} for x, y in all_data.items()]

    credit_average = get_average(credit_transactions)
    debit_average = get_average(debit_transactions)

    datasets = [
        {
            "label": f"Credit({credit_average})",
            "borderColor": "#f67019",
            "data": credit_data,
        },
        {
            "label": f"Debit({debit_average})",
            "borderColor": "#537bc4",
            "data": debit_data,
        },
        {"label": "All", "borderColor": "#58595b", "data": all_data,},
    ]

    return JsonResponse(data={"labels": labels, "datasets": datasets})
