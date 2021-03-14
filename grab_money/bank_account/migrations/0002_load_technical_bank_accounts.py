from django.db import migrations
from django.core.management import call_command


def load_fixture(apps, schema_editor):
    call_command('loaddata', 'technical_bank_accounts')


def unload_fixture(apps, schema_editor):
    "Brutally deleting all entries for this model..."

    BankAccount = apps.get_model("bank_account", "BankAccount")
    for _id in [20, 21, 22, 23, 24]:
        BankAccount.objects.get(pk=_id).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('category', '0003_load_categories'),
        ('bank_account', '0001_initial'),
        ('users', '0002_load_technical_users'),
        ('currency', '0003_load_currencies'),
    ]

    operations = [
        migrations.RunPython(load_fixture, reverse_code=unload_fixture),
    ]
