# Generated by Django 2.2.16 on 2022-04-26 13:59

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0024_auto_20220426_0958'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnidadeDeMedida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('alterado_em', models.DateTimeField(auto_now=True, verbose_name='Alterado em')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('nome', models.CharField(max_length=160, verbose_name='Nome')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]