# Generated by Django 2.2.16 on 2022-05-06 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0025_auto_20220506_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dotacaoorcamentaria',
            name='conta_despesa',
            field=models.CharField(max_length=8, verbose_name='Conta Despesa'),
        ),
    ]