from rest_framework import serializers

from ...models import ModeloAteste
from .grupo_verificacao_serializer import GrupoVerificacaoSerializer


class ModeloAtesteSerializer(serializers.ModelSerializer):
    grupos_de_verificacao = GrupoVerificacaoSerializer(many=True)

    class Meta:
        model = ModeloAteste
        fields = ('uuid', 'titulo', 'criado_em', 'grupos_de_verificacao')
        # exclude = ('id',)
