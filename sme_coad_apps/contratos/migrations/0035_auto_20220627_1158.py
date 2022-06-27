# Generated by Django 2.2.16 on 2022-06-27 14:58

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0034_auto_20220627_1151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contrato',
            name='tipo_servico',
        ),
        migrations.AddField(
            model_name='contrato',
            name='descricao_objeto',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='contrato',
            name='objeto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='contratos_do_tipo', to='contratos.Objeto', verbose_name='objeto'),
        ),
        migrations.AlterField(
            model_name='colunascontrato',
            name='colunas_array',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=[{'field': 'termo_contrato', 'header': 'TC'}, {'field': 'processo', 'header': 'Processo'}, {'field': 'objeto.nome', 'header': 'Obejto'}, {'field': 'empresa_contratada.nome', 'header': 'Empresa'}, {'field': 'estado_contrato', 'header': 'Estado do Contrato'}, {'field': 'data_encerramento', 'header': 'Data Encerramento'}], verbose_name='Lista de campos'),
        ),
    ]