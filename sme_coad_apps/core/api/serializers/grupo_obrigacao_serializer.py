from rest_framework import serializers

from ...models import Edital, GrupoObrigacao
from .obrigacao_serializer import ObrigacaoSerializer


class GrupoObrigacaoSerializer(serializers.ModelSerializer):
    edital = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        queryset=Edital.objects.all()
    )
    itens_de_obrigacao = ObrigacaoSerializer(many=True)

    class Meta:
        model = GrupoObrigacao
        fields = ('uuid', 'nome', 'edital', 'itens_de_obrigacao')


class GrupoObrigacaoSerializerCreate(serializers.ModelSerializer):
    edital = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        queryset=Edital.objects.all()
    )
    itens_de_obrigacao = ObrigacaoSerializer(many=True)

    def create(self, validated_data):
        grupo = GrupoObrigacao.objects.create(**validated_data)
        return grupo

    class Meta:
        model = GrupoObrigacao
        fields = ('uuid', 'nome', 'edital')
