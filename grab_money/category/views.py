# Django:
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

# Firstparty:
from grab_money.base.views import universal_error
from grab_money.transaction.models import Transaction

# Localfolder:
from .forms import CategoryForm, EditCategoryForm
from .models import Category


@login_required(login_url="/accounts/login/")
def category_list(request):
    categories = Category.objects.filter()
    context = {"categories": categories}
    return render(request, "category/list.html", context)


@login_required(login_url="/accounts/login/")
def category_create(request):
    context = {"form": CategoryForm()}
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.owner = request.user
            new_category.save()
            return redirect("category:category-list")
    elif request.method == "GET":
        return render(request, "category/category_create.html", context)


@login_required(login_url="/accounts/login/")
def category_edit(request, id):
    category = Category.objects.get(pk=id)
    if request.method == "POST":
        if request.user != category.owner:
            return universal_error(request, context={"code": 403})
        form = EditCategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect("category:category-list")
    else:
        if request.user != category.owner:
            return universal_error(request, context={"code": 403})
        form = EditCategoryForm(instance=category)
    return render(request, "category/category_edit.html", {"form": form})


@login_required(login_url="/accounts/login/")
def category_delete(request, id):
    category = Category.objects.get(pk=id)
    if request.user != category.owner:
        return universal_error(request, context={"code": 403})
    category.delete()
    return redirect("category:category-list")


@login_required(login_url="/accounts/login/")
def category_detail(request, id):
    category = Category.objects.get(pk=id)
    transactions = Transaction.objects.filter(category=id)
    context = {"category": category, "transactions": transactions}
    return render(request, "category/category_detail.html", context)
