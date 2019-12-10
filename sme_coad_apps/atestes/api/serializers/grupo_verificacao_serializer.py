from rest_framework import serializers

from .intens_verificacao_serializer import ItensVerificacaoSerializer
from ...models import GrupoVerificacao, ModeloAteste


class GrupoVerificacaoSerializer(serializers.ModelSerializer):
    modelo = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        queryset=ModeloAteste.objects.all()
    )
    itens_de_verificacao = ItensVerificacaoSerializer(many=True)

    class Meta:
        model = GrupoVerificacao
        fields = ('uuid', 'nome', 'modelo', 'itens_de_verificacao')


class GrupoVerificacaoSerializerCreate(serializers.ModelSerializer):
    modelo = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        queryset=ModeloAteste.objects.all()
    )
    itens_de_verificacao = ItensVerificacaoSerializer(many=True)

    def create(self, validated_data):
        grupo = GrupoVerificacao.objects.create(**validated_data)
        return grupo

    class Meta:
        model = GrupoVerificacao
        fields = ('uuid', 'nome', 'modelo')
