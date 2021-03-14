# Stdlib:
import csv
import re
import time
from copy import deepcopy
from datetime import datetime
from io import BytesIO
from time import mktime, strptime

# Django:
from django.shortcuts import get_list_or_404, get_object_or_404

# Firstparty:
from grab_money.bank_account.models import BankAccount
from grab_money.category.models import Category
from grab_money.currency.models import Currency
from grab_money.transaction.models import Transaction

# Localfolder:
from .base_parser import BaseParser


class AlfaBankAccountCSVParser(BaseParser):
    def parse(self, stream):
        csvfile = (stream.file.read()).decode("1251")
        transactions = csvfile.split("\n")

        # Get account number
        account_number = re.search(r"Account number:.{0,34}", transactions[0])[0].split(
            ":"
        )[1]
        transactions.remove(transactions[1])

        # Find transactions where money were spent on items or services
        items_n_services_list = [
            transaction.split(";")[:-2]
            for transaction in transactions
            if transaction.find("Покупка товара / получение услуг") != -1
        ]
        for item in items_n_services_list:
            item[1] = re.split(r"Покупка товара \/ получение услуг    ", item[1])[1]
            item[2] = item[2][1:]
        items_n_services = [
            {
                "date": datetime.fromtimestamp(
                    mktime(time.strptime(item[0].replace(".", " "), "%d %m %Y"))
                ),
                "account_from": account_number,
                "account_to": "Unknown",
                "category": "Unknown",
                "amount": item[2],
                "description": item[1],
                "keyword": item[1],
            }
            for item in items_n_services_list
        ]

        # Find cash replenishment transactions
        income_list = [
            transaction.split(";")
            for transaction in transactions
            if transaction.find("ПОПОЛНЕНИЕ КАРТСЧЕТОВ") != -1
        ]
        income = [
            {
                "date": datetime.fromtimestamp(
                    mktime(time.strptime(transaction[0].replace(".", " "), "%d %m %Y"))
                ),
                "account_from": "Unknown",
                "account_to": account_number,
                "category": "Unknown",
                "amount": transaction[2],
                "description": "Cash replenishment",
                "keyword": "Replenishment",
            }
            for transaction in income_list
        ]

        # Find cash withdrawal transactions
        outcome_list = [
            transaction.split(";")
            for transaction in transactions
            if transaction.find("Получение денег") != -1
        ]
        outcome = [
            {
                "date": datetime.fromtimestamp(
                    mktime(time.strptime(transaction[0].replace(".", " "), "%d %m %Y"))
                ),
                "account_from": account_number,
                "account_to": "Unknown",
                "category": "Unknown",
                "amount": transaction[2][1:],
                "description": "Cash withdrawal",
                "keyword": "Withdraw",
            }
            for transaction in outcome_list
        ]
        return items_n_services + income + outcome

    def store_transactions(self, transactions, owner):
        for transaction in transactions:
            data = deepcopy(transaction)

            # Copy data for JSON
            data["data"] = deepcopy(data)

            if data.get("account_from") == "Unknown":
                all_transactions_with_unknown = Transaction.objects.filter(owner=owner)
                all_transactions = [
                    [transaction.keyword, transaction.category]
                    for transaction in all_transactions_with_unknown
                    if transaction.category.category_name != "Unknown"
                ]
                if all_transactions != []:
                    keywords = [transaction[0] for transaction in all_transactions]
                    if data.get("keyword") in keywords:
                        for transaction in all_transactions:
                            if transaction[0] == data.get("keyword"):
                                data.update(
                                    {
                                        "category": transaction[1],
                                        "account_from": get_object_or_404(
                                            BankAccount, name="Unknown"
                                        ),
                                    }
                                )

                    else:
                        data.update(
                            {
                                "account_from": get_object_or_404(
                                    BankAccount, name="Unknown"
                                )
                            }
                        )
                else:
                    data.update(
                        {"account_from": get_object_or_404(BankAccount, name="Unknown")}
                    )
            else:
                data.update(
                    {
                        "account_from": get_object_or_404(
                            BankAccount, number_account=data.get("account_from")
                        )
                    }
                )

            if data.get("account_to") == "Unknown":
                all_transactions_with_unknown = Transaction.objects.filter(owner=owner)
                all_transactions = [
                    [transaction.keyword, transaction.category]
                    for transaction in all_transactions_with_unknown
                    if transaction.category.category_name != "Unknown"
                ]
                if all_transactions != []:
                    keywords = [transaction[0] for transaction in all_transactions]
                    if data.get("keyword") in keywords:
                        for transaction in all_transactions:
                            if transaction[0] == data.get("keyword"):
                                data.update(
                                    {
                                        "category": transaction[1],
                                        "account_to": get_object_or_404(
                                            BankAccount, name="Unknown"
                                        ),
                                    }
                                )
                    else:
                        data.update(
                            {
                                "account_to": get_object_or_404(
                                    BankAccount, name="Unknown"
                                )
                            }
                        )
                else:
                    data.update(
                        {"account_to": get_object_or_404(BankAccount, name="Unknown")}
                    )
            else:
                data.update(
                    {
                        "account_to": get_object_or_404(
                            BankAccount, number_account=data.get("account_to")
                        )
                    }
                )

            data["owner"] = owner
            if data.get("category") == "Unknown":
                data.update({"category": Category.objects.get(category_name="Unknown")})

            # Update data dict for success transaction save
            data["data"].update(
                {
                    "date": data.get("date").isoformat(),
                    "category": data.get("category").category_name,
                    "account_from": data.get("account_from").name,
                    "account_to": data.get("account_to").name,
                }
            )

            # Transaction save
            new_transaction = Transaction(**data)
            new_transaction.save()
