# Generated by Django 2.2.4 on 2019-11-08 19:13

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('contratos', '0020_merge_20191106_1452'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParametrosNotificacoesVigencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('alterado_em', models.DateTimeField(auto_now=True, verbose_name='Alterado em')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('estado_contrato', models.CharField(blank=True, choices=[('EMERGENCIAL', 'Emergencial'),
                                                                          ('EXCEPCIONAL', 'Excepcional'),
                                                                          ('ULTIMO_ANO', 'Último Ano'),
                                                                          ('VIGENTE', 'Vigente')], default='',
                                                     max_length=15, verbose_name='Para contratos com estado')),
                ('vencendo_em', models.PositiveSmallIntegerField(blank=True, default=0, null=True,
                                                                 verbose_name='Vencendo a partir de (dias)')),
                ('repetir_notificacao_a_cada', models.PositiveSmallIntegerField(blank=True, default=0, null=True,
                                                                                verbose_name='Repetir notificação a cada (dias)')),
            ],
            options={
                'verbose_name': 'Parâmetro de notificação de vigência',
                'verbose_name_plural': 'Parâmetros de notificação de vigência',
                'unique_together': {('estado_contrato', 'vencendo_em')},
            },
        ),
    ]