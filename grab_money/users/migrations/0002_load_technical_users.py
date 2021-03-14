from django.db import migrations
from django.core.management import call_command


def load_fixture(apps, schema_editor):
    call_command('loaddata', 'technical_users')


def unload_fixture(apps, schema_editor):
    "Brutally deleting all entries for this model..."

    User = apps.get_model("users", "User")
    User.objects.get(pk=1).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_fixture, reverse_code=unload_fixture),
    ]
