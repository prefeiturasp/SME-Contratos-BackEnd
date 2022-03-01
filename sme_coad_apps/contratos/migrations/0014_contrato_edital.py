# Generated by Django 2.2.4 on 2020-05-29 22:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20200529_1017'),
        ('contratos', '0013_merge_20200527_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrato',
            name='edital',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='contartos_do_edital', to='core.Edital'),
        ),
    ]
