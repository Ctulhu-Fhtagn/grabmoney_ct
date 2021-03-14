# Stdlib:
import csv
import shutil
from pathlib import Path

# Thirdparty:
import dateparser

# Localfolder:
from .base_parser import BaseParser

# from grab_money.bank_account.models import BankAccount
# from grab_money.category.models import Category
# from grab_money.currency.models import Currency
# from grab_money.transaction.models import Transaction


class PriorbankCSVParser(BaseParser):
    def parse(self, stream):

        OPERATION_IDENTIFIER = "Операции по"
        BLOCKED_OPERATION_IDENTIFIER = "Заблокированные суммы по"
        DELIMETER = ";"

        def line_is_start_contract(line):
            return line.startswith(OPERATION_IDENTIFIER) or line.startswith(
                BLOCKED_OPERATION_IDENTIFIER
            )

        def grab_contracts(lines):
            contracts = []
            for line in lines:
                if line_is_start_contract(line) and line not in contracts:
                    contracts += [line]
            return contracts

        def grab_header(lines):
            result = []
            for line in lines:
                if line_is_start_contract(line):
                    break
                result += [line]
            return result

        def delete_unused(lines):
            result = lines[0:2]
            for line in lines[2:]:
                data = line.split(DELIMETER)
                if line.strip():
                    res = dateparser.parse(data[0])
                    if res is None:
                        break
                    else:
                        result += [line]
                else:
                    result += [line]
            return result

        def grab_contract(lines, contract):
            result = []
            start = False
            for i, line in enumerate(lines):
                if line_is_start_contract(line):
                    if line == contract:
                        start = True
                    elif line != contract and start:
                        break
                if i == (len(lines) - 1):
                    break
                if start:
                    result += [line]
            return delete_unused(result)

        def convert_to_prefix(key):
            result = str(key).strip().split(".")[-1]
            if BLOCKED_OPERATION_IDENTIFIER in key:
                result = "B_" + result
            elif OPERATION_IDENTIFIER in key:
                result = "O_" + result
            return result

        def split_file(x):
            operations = {}
            with open(x, encoding="windows-1251") as file:
                lines = file.readlines()
                contracts = grab_contracts(lines)
                operations["header"] = grab_header(lines)
                for contract in contracts:
                    operations[contract] = grab_contract(lines, contract)
            folder = (
                (x.resolve() / "..").resolve() / ("PARSED_" + x.name.split(".")[0])
            ).resolve()
            if folder.exists() and folder.is_dir():
                shutil.rmtree(folder)
            folder.mkdir()
            for key in operations.keys():
                prefix = convert_to_prefix(key)
                filename = (folder / (prefix + ".csv")).resolve()
                with open(filename, "w", encoding="windows-1251") as f:
                    if key == "header":
                        f.writelines(operations[key])
                    else:
                        f.writelines(operations[key][1:])

        def clean():
            p = Path(".")
            for x in p.iterdir():
                if x.suffixes == [".csv"] and (
                    x.name.startswith("B_") or x.name.startswith("O_")
                ):
                    x.unlink()
                if x.is_dir() and x.name.startswith("PARSED_"):
                    shutil.rmtree(x)

        clean()

        p = Path(".")
        for x in p.iterdir():
            if (
                x.suffixes == [".csv"]
                and not x.name.startswith("B_")
                and not x.name.startswith("O_")
            ):
                split_file(x)

        files_to_process = []

        p = Path(".")
        for x in p.iterdir():
            if x.is_dir() and x.name.startswith("PARSED"):
                for file in x.iterdir():
                    if not file.name.startswith("header"):
                        files_to_process += [file]

        result = {}

        for file in files_to_process:
            key = file.name.split(".")[0]
            if key not in result:
                result[key] = []

            with open(file, "r", encoding="windows-1251") as f:
                lines = f.readlines()
                if not result[key]:
                    result[key] += lines[0]
                for line in lines[1:]:
                    if line.strip():
                        result[key] += line

        for key, value in result.items():
            result_file = p / (key + ".csv")
            with open(result_file, "w", encoding="windows-1251") as r:
                r.writelines(value)

            p = Path(".")
            for x in p.iterdir():

                with open(x, "r", encoding="windows-1251") as csv_file:
                    # csv_reader = csv.reader(codecs.interdecode(stream, 'windows-1251'), delimiter=';')
                    csv_reader = csv.reader(csv_file, delimiter=";")
                    data = []
                    for line in csv_reader:
                        data.append(line)

                # card_index = []
                # for line in data:
                #     if len(line) == 1:
                #         card_index.append(data.index(line))
                #         card_list.append(line)
                #
                # transaction_index = []
                # for line_tr in data:
                #     if len(line_tr) == 10:
                #         transaction_index.append(data.index(line_tr))
                #         input_list.append(line_tr)
                #
                # re_account_from = r"(?P<card_number>\s[.]{8}[0-9]{4})"
                # account_from = re.finditer(re_account_from, str(card_list), re.MULTILINE)
                # for matchNum, match in enumerate(account_from, start=1):
                #     card = {}
                #     card['account_from'] = match.group()
                #     output_list_card.append(card)
                #
                # list_of_date = []
                # headers = input_list[0]
                # for lin in input_list[1:]:
                #     index_lin = int(input_list.index(lin) + 1)
                #     list_of_date.append(dict(zip(headers, input_list[index_lin])))
                #     if index_lin == len(input_list) - 1:
                #         break
