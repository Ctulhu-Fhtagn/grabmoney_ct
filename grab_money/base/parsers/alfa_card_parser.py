# Stdlib:
import codecs
import csv
import re
import tempfile
from copy import deepcopy
from datetime import datetime

# Django:
from django.utils.timezone import make_aware

# Firstparty:
from grab_money.category.models import Category
from grab_money.currency.models import Currency
from grab_money.transaction.models import Transaction

# Localfolder:
from .base_parser import BaseParser


class AlfaBankCardCSVParser(BaseParser):
    def parse(self, stream):

        lines = stream.readlines()
        general_header = lines[:2]
        transactions_lines = lines[2:]
        transactions_file = tempfile.TemporaryFile()
        transactions_file.writelines(transactions_lines)
        transactions_file.seek(0)

        csv_reader = csv.DictReader(
            codecs.iterdecode(transactions_file, "Windows-1251"), delimiter=";"
        )

        output_list = []

        reg_card = r"[0-9]\*{11}[0-9]{4}"
        card_number = re.finditer(
            reg_card, general_header[0].decode("Windows-1251"), re.MULTILINE
        )
        card = "Unknown"
        for matchNum, match in enumerate(card_number, start=1):
            card = match.group()
        balance = (
            general_header[0]
            .decode("Windows-1251")
            .split("Available balance:")[1]
            .strip()
            .replace(";", "")
        )
        balance, balance_currency = balance.split(" ")

        for row in csv_reader:

            output = dict(
                account_from=card,
                account_to=row["Details"],
                date=datetime.strptime(row["Transaction time"], "%d.%m.%Y %H:%M:%S"),
                amount=float(row["Amount in operation currency"]),
                currency=row["Currency code"],
                transaction_number=row["Transaction number"],
                operation_type=row["Operation type"],
                country=row["Country"],
                city=row["City"],
                openning_balance=float(balance),
                openning_balance_currency=balance_currency,
            )
            output_list.append(output)

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

            account_from = self.create_and_save_account(
                owner=owner,
                name=transaction["account_from"],
                currency=Currency.objects.get(
                    short_unit_label=transaction["openning_balance_currency"]
                ),
            )
            data["account_from"] = account_from

            category, category_account = Category.search_by_keyword(
                transaction["account_to"]
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
