# Generated by Django 2.2.16 on 2022-06-02 06:20

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0031_auto_20220527_1712'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProdutosAta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('alterado_em', models.DateTimeField(auto_now=True, verbose_name='Alterado em')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('quantidade_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('valor_unitario', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('valor_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('anexo', models.FileField(blank=True, default='', upload_to='uploads/')),
                ('ata', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produtos', to='contratos.Ata')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produtos_ata', to='contratos.Produto')),
            ],
            options={
                'verbose_name': 'Produto de Ata',
                'verbose_name_plural': 'Produtos de Atas',
            },
        ),
    ]