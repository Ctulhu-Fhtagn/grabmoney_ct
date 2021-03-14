# Django:
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Localfolder:
from .models import Currency


@login_required(login_url="/accounts/login/")
def currency_list(request):
    currencies = Currency.objects.all()
    context = {"currencies": currencies}
    return render(request, "currency/list.html", context)
