# Generated by Django 3.0.5 on 2020-05-16 07:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transaction', '0004_auto_20200510_1003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='owner',
            field=models.ForeignKey(blank=True, default='2', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
