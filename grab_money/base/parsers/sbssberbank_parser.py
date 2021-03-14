# Stdlib:
from copy import deepcopy
from datetime import datetime
from re import MULTILINE, findall, finditer

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


class SberbankPDFParser(BaseParser):
    def parse(self, stream):

        pdf = pdfplumber.load(stream)
        # test_str = pdf.pages[2].extract_text()
        number_of_pages = len(pdf.pages)

        test_str = str()

        for i in range(0, number_of_pages):
            test_str += pdf.pages[i].extract_text()

        # regular expression for salary

        regex_salary = (
            r"(?P<russion_description>[ЁёА-я]+ [ЁёА-я]+)\n"
            r"(?P<date_of_transaction>\d{2}\.\d{2}\.\d{4}) *(?P<time_of_transaction>\d{2}\:\d{2}\:\d{2}) *(?P<date_according_to_bank>\d{2}\.\d{2}\.\d{4}) *(?P<time_according_to_bank>\d{2}\:\d{2}\:\d{2}) *\W+.\.. (?P<currency>\w+) (?P<value_spended_absolute>\-\d*\.\d*|\d*\.\d*) *(?P<value_of_bank_account>\d*\.\d*) *\n"
            r"\w*\n"
            r" *\"\w* \n"
            r"\w* \w\n"
            r"\w* \w* \w*\W*\n"
            r"\w* \w*\n"
            r" *(?P<account_from>\:\d{9})"
        )

        matches_salary = finditer(regex_salary, test_str, MULTILINE)

        # regular expression for bank_account_from

        regex_iban = r"\bIBAN\b *(?P<bank_account_from>\w*)"

        iban = findall(regex_iban, test_str)[0]

        # regular expression for Yandex.Taxi

        regex_Taxi = (
            r"(?P<russion_description>[ЁёА-я]+)\n"
            r"(?P<date_of_transaction>\d{2}\.\d{2}\.\d{4}) *(?P<time_of_transaction>\d{2}\:\d{2}\:\d{2}) *(?P<date_according_to_bank>\d{2}\.\d{2}\.\d{4}) *(?P<time_according_to_bank>\d{2}\:\d{2}\:\d{2}) *(?P<value_spended_absolute>\-\d*\.\d*) (?P<currency>\w+) (?P<value_spended_byn>\-\d*\.\d*) *(?P<value_of_bank_account>\d*\.\d*)\n"
            r"\w* *\n"
            r"\W*(?P<vendor>[a-zA-Z]*\.[a-zA-Z]*)"
        )

        matches_Taxi = finditer(regex_Taxi, test_str, MULTILINE)

        # regular expression for ATM

        regex_ATM = (
            r"(?P<russion_description>[ЁёА-я]+)\n"
            r"(?P<date_of_transaction>\d{2}\.\d{2}\.\d{4}) *(?P<time_of_transaction>\d{2}\:\d{2}\:\d{2}) *(?P<date_according_to_bank>\d{2}\.\d{2}\.\d{4}) *(?P<time_according_to_bank>\d{2}\:\d{2}\:\d{2}) *\: (?P<ATM_details>\w*\.\w*\W*\d* \w*\-\d* \w*|\w*\.\w*\/\d* \w*\.\d* \w*|\"\w*|\w* \"\w*\"\w* \w*\-\d*) *(?P<value_spended_absolute>\-\d*\.\d*) (?P<currency>\w+) (?P<value_spended_byn>\-\d*\.\d*) *(?P<value_of_bank_account>\d*\.\d*)"
        )
        matches_ATM = finditer(regex_ATM, test_str, MULTILINE)

        # regular expression for operations with vendor

        regex_vendor = (
            r"(?P<russion_description>[ЁёА-я]+)\n"
            r"(?P<date_of_transaction>\d{2}\.\d{2}\.\d{4}) *(?P<time_of_transaction>\d{2}\:\d{2}\:\d{2}) *(?P<date_according_to_bank>\d{2}\.\d{2}\.\d{4}) *(?P<time_according_to_bank>\d{2}\:\d{2}\:\d{2}) *\: *(?P<value_spended_absolute>\-\d*\.\d*) (?P<currency>\w+) (?P<value_spended_byn>\-\d*\.\d*) *(?P<value_of_bank_account>\d*\.\d*) *\n"
            r"(?P<vendor>^\w* \"\w* \d\"|\w+ \"\w*\" \w*|\w* \"\w* \d*\"|\w* \"\w*\"|\w* \w*\.\w*|\w* \w* \w*|\w*\.\w*|\w* \w*\-\w*|\w* \w*|\w*)"
        )

        matches_vendor = finditer(regex_vendor, test_str, MULTILINE)

        # regular expression for operations with other vendor(with :USL)

        regex_vendor_other = (
            r"(?P<russion_description>[ЁёА-я]+)\n"
            r"(?P<date_of_transaction>\d{2}\.\d{2}\.\d{4}) *(?P<time_of_transaction>\d{2}\:\d{2}\:\d{2}) *(?P<date_according_to_bank>\d{2}\.\d{2}\.\d{4}) *(?P<time_according_to_bank>\d{2}\:\d{2}\:\d{2}) *\: \w* *(?P<value_spended_absolute>\-\d*\.\d*) (?P<currency>\w+) (?P<value_spended_byn>\-\d*\.\d*) *(?P<value_of_bank_account>\d*\.\d*)\n"
            r"(?P<vendor>^\w* \w* \w*\-\w*|\w* \w* \w* \w*)"
        )

        matches_vendor_other = finditer(regex_vendor_other, test_str, MULTILINE)

        # regular expression for operations money transit

        regex_new_money = (
            r"(?P<russion_description>[ЁёА-я]+)\n"
            r"(?P<date_of_transaction>\d{2}\.\d{2}\.\d{4}) *(?P<time_of_transaction>\d{2}\:\d{2}\:\d{2}) *(?P<date_according_to_bank>\d{2}\.\d{2}\.\d{4}) *(?P<time_according_to_bank>\d{2}\:\d{2}\:\d{2}) *(?P<value_spended_absolute>\d*\.\d*) (?P<currency>\w+) (?P<value_spended_byn>\d*\.\d*) *(?P<value_of_bank_account>\d*\.\d*)"
        )

        matches_new_money = finditer(regex_new_money, test_str, MULTILINE)

        data = []

        for match in matches_Taxi:
            data.append(match.groupdict())

        for match in matches_ATM:
            data.append(match.groupdict())

        for match in matches_vendor:
            data.append(match.groupdict())

        for match in matches_vendor_other:
            data.append(match.groupdict())

        for match in matches_new_money:
            data.append(match.groupdict())

        for match in matches_salary:
            data.append(match.groupdict())

        print(data)

        data_into_transactions = []

        for i in data:
            d = {}

            if i.get("vendor") == None:
                if (
                    i.get("russion_description")
                    == "Зачислениевыплат входящихвФЗППредставительство"
                ):
                    d["account_from"] = i.get("account_from")[1:]
                    d["description"] = i.get("russion_description")
                    d["account_to"] = iban
                if (
                    i.get("russion_description")
                    == "Пополнениекарточногосчетапокарточке"
                ):
                    d["account_from"] = iban
                    d["description"] = i.get("russion_description")
                    d["account_to"] = "replenishment_of_balance"
                if i.get("russion_description") == "Снятиеналичных":
                    d["account_from"] = iban
                    d["description"] = (
                        i.get("russion_description") + " " + i.get("ATM_details")
                    )
                    d["account_to"] = "cash_withdrawal"
            else:
                d["description"] = str(
                    i.get("russion_description") + " " + i.get("vendor")
                )
                d["account_to"] = i.get("vendor")
                d["account_from"] = iban
            d["date"] = datetime.strptime(
                i.get("date_of_transaction") + " " + i.get("time_of_transaction"),
                "%d.%m.%Y %H:%M:%S",
            ).isoformat()
            d["amount"] = abs(float(i.get("value_spended_absolute")))
            d["openning_balance_currency"] = i.get("currency")
            data_into_transactions.append(d)

        return data_into_transactions

    def store_transactions(self, transactions, owner):

        for transaction in transactions:

            data = dict(
                data=deepcopy(transaction),
                description=transaction.get("description"),
                keyword=transaction.get("account_to"),
            )
            data["date"] = make_aware(transaction["date"])
            data["amount"] = transaction["amount"]
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
            tr = Transaction(**data)
            tr.save()
