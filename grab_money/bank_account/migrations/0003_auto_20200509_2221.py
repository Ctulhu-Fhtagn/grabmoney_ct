# Generated by Django 3.0.5 on 2020-05-09 22:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bank_account', '0002_load_technical_bank_accounts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccount',
            name='owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
