
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='mcc_code',
            field=models.CharField(blank=True, max_length=25),
        ),
    ]
