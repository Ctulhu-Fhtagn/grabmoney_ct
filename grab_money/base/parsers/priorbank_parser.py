# Stdlib:
import re
from copy import deepcopy
from datetime import datetime

# Thirdparty:
import pdfplumber

# Firstparty:
# Firstparty
from grab_money.bank_account.models import BankAccount
from grab_money.category.models import Category
from grab_money.currency.models import Currency
from grab_money.transaction.models import Transaction

# Localfolder:
from .base_parser import BaseParser


class PriorbankPDFParser(BaseParser):
    def parse(self, stream):
        pdf = pdfplumber.load(stream)
        first_tables = pdf.pages[0].extract_tables()
        second_tables = pdf.pages[1].extract_tables()[:1]
        info = list(pdf.pages[0].extract_text()[:350].split())
        card_number = info[15][-4:]
        current_balance = float(info[36])
        clear_list = []

        for single_table in first_tables:
            if single_table[0][0] == "Транзакции":
                clear_list.append(single_table[2:])

        clear_list += second_tables
        output_list = []

        for operations in clear_list:
            for operation in operations:
                operation_dict = {}
                operation_dict["date"] = datetime.strptime(operation[4], "%d.%m.%Y")
                operation_dict["description"] = operation[1]
                operation_dict["currency"] = operation[3]
                if float(operation[6]) >= 0:
                    operation_dict["account_to"] = card_number
                    operation_dict["account_from"] = "Enrollment"
                else:
                    operation_dict["account_to"] = operation[1]
                    operation_dict["account_from"] = card_number
                output_list.append(operation_dict)
                operation_dict["amount"] = abs(float(operation[6]))
        return output_list

    def store_transactions(self, transactions, owner):
        account_from = None
        for transaction in transactions:
            data = dict(
                data=deepcopy(transaction),
                description=transaction["account_to"],
                keyword=transaction["account_to"],
            )

            data["owner"] = owner

            account_from, account_from_created = BankAccount.objects.get_or_create(
                owner=owner,
                name=transaction["account_from"],
                type="Debit",
                opening_debit=0,
                opening_credit=0,
                currency=Currency.objects.get(short_unit_label=transaction["currency"]),
            )
            data["account_from"] = account_from

            category, category_account = Category.search_by_keyword(
                transaction["account_to"]
            )
            data["category"] = category
            data["account_to"] = category_account
            data["date"] = transaction["date"]

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
        if account_from is not None:
            account_from.balance = 0
            account_from.save()
