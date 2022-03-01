# Generated by Django 2.2.4 on 2019-11-28 20:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='servidor',
            name='servidor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='servidor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='nucleo',
            name='chefe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='chefe_nucleo', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='nucleo',
            name='divisao',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Divisao'),
        ),
        migrations.AddField(
            model_name='nucleo',
            name='suplente_chefe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='suplente_chefe_nucleo', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='divisao',
            name='diretor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='diretor_divisao', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='divisao',
            name='suplente_diretor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='suplente_diretor_divisao', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='coadassessor',
            name='assessor',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='assessor_coad', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='coadassessor',
            name='coad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessores', to='core.Coad'),
        ),
        migrations.AddField(
            model_name='coad',
            name='coordenador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='coordenador_coad', to=settings.AUTH_USER_MODEL),
        ),
    ]
