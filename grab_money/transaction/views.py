# Django:
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

# Firstparty:
from grab_money.base.views import universal_error
from grab_money.category.models import Category, CategoryKeyword

# Localfolder:
from .forms import AssignCategoryTransactionForm, EditTransactionForm, TransactionForm
from .models import DONE, DRAFT, FAILED, Transaction


@login_required(login_url="/accounts/login/")
def transaction_create(request):
    context = {"form": TransactionForm()}
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            new_transaction = form.save(commit=False)
            new_transaction.owner = request.user
            new_transaction.save()
        return redirect("transaction:transaction-list")
    elif request.method == "GET":
        return render(request, "transaction/create.html", context)


@login_required(login_url="/accounts/login/")
def transaction_edit(request, id, category_id=None):
    transaction = Transaction.objects.get(pk=id)
    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if request.user != transaction.owner:
            return universal_error(request, context={"code": 403})
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.save()
            if category_id is not None:
                return redirect("category:category-detail", id=category_id)
            return redirect("transaction:transaction-list")
    else:
        form = EditTransactionForm(instance=transaction, category_id=category_id)

        return render(request, "transaction/edit.html", {"form": form})


@login_required(login_url="/accounts/login/")
def transaction_delete(request, id):
    transaction = Transaction.objects.get(pk=id)
    if request.user != transaction.owner:
        return universal_error(request, context={"code": 403})
    transaction.delete()
    return redirect("transaction:transaction-list")


def get_unknown_transactions(user):
    return Transaction.objects.filter(
        owner=user, status=DRAFT, category=Category.objects.get(pk=1)
    )


@login_required(login_url="/accounts/login/")
def transaction_list(request):
    transactions = Transaction.objects.filter(owner=request.user, status=DONE)
    unknown_transactions = get_unknown_transactions(request.user)
    context = {
        "transactions": transactions,
        "len_unknown_transactions": len(unknown_transactions),
    }
    return render(request, "transaction/list.html", context)


@login_required(login_url="/accounts/login/")
def transaction_unknown_list(request):
    act_form = AssignCategoryTransactionForm()
    transactions = get_unknown_transactions(request.user)
    context = {"transactions": transactions, "act_form": act_form}
    return render(request, "transaction/unknown_transactions_list.html", context)


@login_required(login_url="/accounts/login/")
def transaction_assign_category(request, id):
    transaction = Transaction.objects.get(pk=id)
    if request.user != transaction.owner:
        return universal_error(request, context={"code": 403})
    if request.method == "POST":
        act_form = AssignCategoryTransactionForm(request.POST)
        if act_form.is_valid():
            category = act_form.cleaned_data["category"]
            # import pdb; pdb.set_trace()
            keyword, created = CategoryKeyword.objects.get_or_create(
                category=category, word=transaction.keyword,
            )
            if created:
                keyword.save()
            category, category_account = Category.search_by_keyword(transaction.keyword)
            transaction.category = category
            transaction.account_to = category_account
            transaction.status = DONE
        else:
            transaction.status = (FAILED,)
        transaction.save()
        Transaction.reprocess_transactions(request.user)
    return redirect("transaction:transaction-unknown-list")


@login_required(login_url="/accounts/login/")
def transaction_detail(request, id):
    transaction = Transaction.objects.get(pk=id)
    if request.user != transaction.owner:
        return universal_error(request, context={"code": 403})
    context = {"transaction": transaction}
    return render(request, "transaction/detail.html", context)
