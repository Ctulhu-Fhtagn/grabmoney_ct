# Django:
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Firstparty:
from grab_money.bank_account.forms import BankAccountForm, EditBankAccountForm
from grab_money.base.views import universal_error

# Localfolder:
from .models import BankAccount


@login_required(login_url="/accounts/login/")
def account_name_list(request):
    bank_accounts = BankAccount.objects.filter(owner=request.user).order_by("id")
    context = {"bank_accounts": bank_accounts}

    return render(request, "bank_account/list.html", context)


@login_required(login_url="/accounts/login/")
def account_name_create(request):

    base_context = {"bank_account_new": BankAccountForm()}
    if request.method == "GET":
        return render(request, "bank_account/list_edit_new.html", base_context)
    elif request.method == "POST":

        form = BankAccountForm(request.POST)
        if form.is_valid():
            bank_account = form.save(commit=False)
            bank_account.owner = request.user
            bank_account.save()
        return HttpResponseRedirect("/bank_account")
    else:
        return universal_error(request, context={"code": 405})


@login_required(login_url="/accounts/login/")
def account_name_delete(request, id):
    bank_account = BankAccount.objects.get(pk=id)

    if request.user != bank_account.owner:
        return universal_error(request, context={"code": 403})
    bank_account.delete()
    return HttpResponseRedirect("/bank_account")


@login_required(login_url="/accounts/login/")
def account_name_edit(request, id):
    bank_account = BankAccount.objects.get(pk=id)
    form = EditBankAccountForm(instance=bank_account)
    if request.method == "GET":
        return render(request, "bank_account/list_edit.html", context={"form": form})
    elif request.method == "POST":
        if request.user != bank_account.owner:
            return universal_error(request, context={"code": 403})

        form = BankAccountForm(request.POST, instance=bank_account)
        if form.is_valid():
            bank_account = form.save(commit=False)
            bank_account.owner = request.user
            bank_account.save()
        return HttpResponseRedirect("/bank_account")
    else:
        return universal_error(request, context={"code": 405})


@login_required(login_url="/accounts/login/")
def account_detail(request, id):
    try:
        account = BankAccount.objects.get(pk=id)
    except BankAccount.DoesNotExist:
        return universal_error(request, context={"code": 404})

    # Check for right request user
    if account.owner != request.user:
        return universal_error(request, context={"code": 403})

    context = {"account": account}
    return render(request, "bank_account/account_detail.html", context)
