# Generated by Django 2.2.4 on 2021-07-21 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0017_auto_20210721_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrato',
            name='valor_total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='dotacaovalor',
            name='valor',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
        ),
    ]