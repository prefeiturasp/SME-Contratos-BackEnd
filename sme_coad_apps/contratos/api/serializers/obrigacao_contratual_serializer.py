from rest_framework import serializers

from ...models import ObrigacaoContratual, Contrato


class ObrigacaoContratualSerializer(serializers.ModelSerializer):
    contrato = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        queryset=Contrato.objects.all()
    )

    class Meta:
        model = ObrigacaoContratual
        fields = ('uuid', 'contrato', 'item', 'obrigacao')


class ObrigacaoContratualCreatorSerializer(serializers.ModelSerializer):
    contrato = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        queryset=Contrato.objects.all()
    )

    class Meta:
        model = ObrigacaoContratual
        fields = '__all__'
