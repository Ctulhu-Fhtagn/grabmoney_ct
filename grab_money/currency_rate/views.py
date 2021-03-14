# Django:
# Stdlib:
import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

# Firstparty:
from grab_money.currency.models import Currency
from grab_money.currency_rate.utils import get_all_currency_rate_date

# Localfolder:
from .forms import CurrencyRateRefreshForm
from .models import CurrencyRate


@login_required(login_url="/accounts/login/")
def currency_rate_list(request, date):

    currencies = Currency.objects.all()
    if date == "today":
        date = datetime.datetime.now().date()
    rates = CurrencyRate.objects.filter(date=date)

    context = {
        "currencies": currencies,
        "rates": rates,
        "date": date,
        "form": CurrencyRateRefreshForm(),
    }

    return render(request, "currency_rate/list.html", context)


@login_required(login_url="/accounts/login/")
def currency_rate_refresh(request):

    if request.method == "POST":
        form = CurrencyRateRefreshForm(request.POST)

        date = form.data["date"]
        rates = get_all_currency_rate_date(date)

        for rate in rates:
            try:
                currency = Currency.objects.get(short_unit_label=rate["abbreviation"])
                if not CurrencyRate.objects.filter(
                    date=date, currency_id=currency
                ).exists():
                    new_rate = CurrencyRate()
                    new_rate.currency_id = currency
                    new_rate.rate = rate["rate"]
                    new_rate.date = date
                    new_rate.scale = rate["scale"]
                    new_rate.save()

            except Currency.DoesNotExist:
                pass

    return redirect("currency_rate:currency-rate-list", date=date)


@login_required(login_url="/accounts/login/")
def currency_rate_detail(request, shortalias):
    currencies = Currency.objects.filter(short_unit_label=shortalias)
    if currencies:
        currency = currencies[0]
        rates = CurrencyRate.objects.filter(currency_id=currency)
        context = {
            "currency": currency,
            "rates": rates,
            "scale": rates and rates[0].scale or False,
        }
        return render(request, "currency_rate/detail.html", context)
    return currency_rate_list(request)
