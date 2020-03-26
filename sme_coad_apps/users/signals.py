from django.db.models.signals import post_save
from django.dispatch import receiver
from ..contratos.models.colunas_contrato import ColunasContrato
from django.contrib.auth import get_user_model
model_user = get_user_model()


@receiver(post_save, sender=model_user)
def colunas_contrato_create(sender, instance, created, *_args, **_kwargss):
    if created:
        ColunasContrato.objects.create(usuario=instance)
