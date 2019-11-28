# Generated by Django 2.2.4 on 2019-11-28 16:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0012_unidade_dre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unidade',
            name='dre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                                    related_name='unidades_da_dre', to='core.Unidade'),
        ),
    ]