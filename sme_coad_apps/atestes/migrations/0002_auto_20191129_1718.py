# Generated by Django 2.2.4 on 2019-11-29 20:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atestes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grupoverificacao',
            name='modelo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grupos_de_verificacao', to='atestes.ModeloAteste'),
        ),
        migrations.AlterField(
            model_name='itensverificacao',
            name='grupo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens_de_verificacao', to='atestes.GrupoVerificacao'),
        ),
    ]
