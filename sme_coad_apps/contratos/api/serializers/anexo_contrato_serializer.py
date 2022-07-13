from rest_framework import serializers

from ...models.contrato import Contrato, AnexoContrato


class AnexoContratolSerializer(serializers.ModelSerializer):
    contrato = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        queryset=Contrato.objects.all()
    )

    class Meta:
        model = AnexoContrato
        exclude = ('id',)
