from rest_framework import serializers

from .obrigacao_serializer import ItemObrigacaoSerializer
from ...models import GrupoObrigacao, Edital


class GrupoObrigacaoSerializer(serializers.ModelSerializer):
    edital = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        queryset=Edital.objects.all()
    )
    itens_de_obrigacao = ItemObrigacaoSerializer(many=True)

    class Meta:
        model = GrupoObrigacao
        fields = ('uuid', 'nome', 'edital', 'itens_de_obrigacao')


class GrupoObrigacaoSerializerCreate(serializers.ModelSerializer):
    edital = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        queryset=Edital.objects.all()
    )
    itens_de_obrigacao = ItemObrigacaoSerializer(many=True)

    def create(self, validated_data):
        grupo = GrupoObrigacao.objects.create(**validated_data)
        return grupo

    class Meta:
        model = GrupoObrigacao
        fields = ('uuid', 'nome', 'edital')
