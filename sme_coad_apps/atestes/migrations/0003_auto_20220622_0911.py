# Generated by Django 2.2.16 on 2022-06-22 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0033_remove_contrato_modelo_ateste'),
        ('atestes', '0002_auto_20191129_1718'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itensverificacao',
            name='grupo',
        ),
        migrations.DeleteModel(
            name='GrupoVerificacao',
        ),
        migrations.DeleteModel(
            name='ItensVerificacao',
        ),
        migrations.DeleteModel(
            name='ModeloAteste',
        ),
    ]
