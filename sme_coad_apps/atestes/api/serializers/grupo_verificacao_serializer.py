from rest_framework import serializers

from ...models import GrupoVerificacao, ModeloAteste
from .intens_verificacao_serializer import ItensVerificacaoSerializer


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
