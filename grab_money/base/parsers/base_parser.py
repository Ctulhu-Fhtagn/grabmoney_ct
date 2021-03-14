# Firstparty:
from grab_money.bank_account.models import BankAccount


class BaseParser:
    def create_and_save_account(self, **data):
        account, account_created = BankAccount.objects.get_or_create(
            **data, **dict(type="Debit", opening_debit=0, opening_credit=0,)
        )
        if account_created:
            account.save()
        return account

    def parse(self, stream):
        pass

    def store_transactions(self, transactions, owner):
        pass
