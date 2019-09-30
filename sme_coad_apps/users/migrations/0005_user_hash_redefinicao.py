# Generated by Django 2.2.4 on 2019-09-25 18:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0004_user_validado'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='hash_redefinicao',
            field=models.TextField(blank=True,
                                   help_text='Campo utilizado para registrar hash na redefinição de senhas'),
        ),
    ]