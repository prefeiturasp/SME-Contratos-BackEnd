# Generated by Django 2.2.16 on 2022-09-13 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0046_auto_20220913_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='tipo_programa',
            field=models.CharField(blank=True, choices=[('ALIMENTACAO_ESCOLAR', 'Alimentação Escolar'), ('LEVE_LEITE', 'Leve Leite')], default='', max_length=25),
        ),
    ]