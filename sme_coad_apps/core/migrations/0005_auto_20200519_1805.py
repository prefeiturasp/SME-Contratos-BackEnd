# Generated by Django 2.2.4 on 2020-05-19 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200519_1529'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unidade',
            name='cep',
        ),
        migrations.RemoveField(
            model_name='unidade',
            name='dre',
        ),
        migrations.RemoveField(
            model_name='unidade',
            name='sigla',
        ),
        migrations.AlterField(
            model_name='unidade',
            name='tipo_unidade',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]