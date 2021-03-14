# Stdlib:
import re
from copy import deepcopy
from datetime import datetime

# Django:
from django.utils.timezone import make_aware

# Thirdparty:
import pdfplumber

# Firstparty:
from grab_money.category.models import Category
from grab_money.currency.models import Currency
from grab_money.transaction.models import Transaction

# Localfolder:
from .base_parser import BaseParser


class MTbankPDFParser(BaseParser):
    def parse(self, stream):

        pdf = pdfplumber.load(stream)
        result = re.findall(r"BY28\w+", pdf.pages[0].extract_text())
        card = result[0]
        mtbank_transactions = []

        j = 1
        for page in pdf.pages:

            tables = pdf.pages[page.page_number - 1].extract_tables()
            for tables_ in tables:
                i = 0

                while True:
                    try:

                        if tables_[i][0] == "T":
                            date = datetime.strptime(tables_[i][2], "%d.%m.%Y")
                            mcc = tables_[i][3]
                            operation_description = re.sub(r"\s+", " ", tables_[i][4])

                            if str(tables_[i][5]) != "None":
                                currency = tables_[i][5]
                            else:
                                currency = tables_[i][6]

                            if (j < 3) & (str(tables_[i][7]) != "None"):
                                currency = tables_[i][6]
                                sum_d = 0
                                sum_k = tables_[i][7]
                            else:

                                i += 1
                                if tables_[i][7] == "-":
                                    sum_k = -float(tables_[i][6])
                                    sum_d = 0
                                elif tables_[i][7] == "+":
                                    sum_d = float(tables_[i][6])
                                    sum_k = 0
                                elif tables_[i][8] == "+":
                                    sum_d = float(tables_[i][7])
                                    sum_k = 0
                                elif tables_[i][8] == "-":
                                    sum_k = -float(tables_[i][7])
                                    sum_d = 0

                            j += 1

                            if sum_d != 0:
                                account_to = card
                                account_from = operation_description
                                amount = sum_d
                            else:
                                account_to = operation_description
                                account_from = card
                                amount = sum_k

                            keyword = operation_description[:100]

                            mtbank_transactions_d = dict(
                                keyword=keyword.strip(),
                                card=card,
                                account_from=account_from,
                                account_to=account_to,
                                date=date,
                                mcc=mcc,
                                operation_description=operation_description,
                                currency=currency,
                                amount=amount,
                            )
                            mtbank_transactions.append(mtbank_transactions_d)

                        i += 1
                    except:
                        break

        return mtbank_transactions

    def store_transactions(self, transactions, owner):
        for transaction in transactions:
            data = dict(
                data=deepcopy(transaction),
                description=transaction["operation_description"],
                keyword=transaction["keyword"],
            )

            data["owner"] = owner

            account_from = self.create_and_save_account(
                owner=owner,
                name=transaction["account_from"],
                currency=Currency.objects.get(short_unit_label=transaction["currency"]),
            )
            data["account_from"] = account_from
            category, category_account = Category.search_by_keyword(
                transaction["keyword"]
            )
            data["category"] = category
            data["account_to"] = category_account

            data["date"] = make_aware(transaction["date"])

            if transaction["currency"] == "BYN":
                data["amount"] = transaction["amount"]
            else:
                data["amount"] = Transaction.currency_exchange(
                    transaction["currency"],
                    transaction["amount"],
                    str(transaction["date"].date()),
                )

            j_date = transaction["date"].isoformat()
            data["data"].update({"date": j_date})
            tr = Transaction(**data)
            tr.save()
