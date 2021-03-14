# Django:
from django.shortcuts import redirect, render

# Localfolder:
from .forms import PARSER_MAPPING, UploadTransactionFileForm


def universal_error(request, context=None):
    # if context is none
    if context is None:
        context = {}
        context["title"] = "Unregistered error"
        context["text"] = "Sorry, we have any problems"
    # if you write any specific context["code"] and ["text"]
    elif "text" in context:
        return render(request, "error.html", context)
    # the most usable errors use by context["code"]
    else:
        if context["code"] == 403:
            context["title"] = "Access denied"
            context["text"] = "You do not have permission for this action"
        elif context["code"] == 404:
            context["title"] = "Page is not found"
            context["text"] = "The requested URL was not found on this server"
        elif context["code"] == 405:
            context["title"] = "Not Allowed"
            context[
                "text"
            ] = "An unsupported HTTP method was used to execute the request"
        elif context["code"] == 500:
            context["title"] = "Server Error"
            context["text"] = "Sorry, something went wrong"

    return render(request, "error.html", context)


def upload_transaction_file(request):
    if request.method == "GET":
        context = dict(form=UploadTransactionFileForm())
        return render(request, "base/upload_transaction_file.html", context)
    elif request.method == "POST":
        form = UploadTransactionFileForm(request.POST)
        if "file" in request.FILES:
            file = request.FILES["file"]
            parser = PARSER_MAPPING[form.data["parser"]]()
            transactions_data = parser.parse(file)
            parser.store_transactions(transactions_data, request.user)
            return redirect("transaction:transaction-list")
        else:
            return universal_error(
                request, context={"code": 500, "text": "Couldn't found file"}
            )
    else:
        return universal_error(request, context={"code": 405})
