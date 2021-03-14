from django.db import migrations
from django.core.management import call_command


def load_fixture(apps, schema_editor):
    call_command('loaddata', 'categories')


def unload_fixture(apps, schema_editor):
    "Brutally deleting all entries for this model..."

    Category = apps.get_model("category", "Category")
    Category.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('category', '0002_auto_20200424_1344'),
        ('users', '0002_load_technical_users'),
    ]

    operations = [
        migrations.RunPython(load_fixture, reverse_code=unload_fixture),
    ]
