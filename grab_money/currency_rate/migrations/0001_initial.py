# Generated by Django 3.0.5 on 2020-05-02 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('currency', '0003_load_currencies'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrencyRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('rate', models.FloatField()),
                ('date', models.DateField()),
                ('currency_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='currency.Currency')),
            ],
        ),
    ]
