from rest_framework import serializers

from .grupo_verificacao_serializer import GrupoVerificacaoSerializer
from .intens_verificacao_serializer import ItensVerificacaoSerializer
from ...models import ModeloAteste, GrupoVerificacao, ItensVerificacao


class ModeloAtesteSerializer(serializers.ModelSerializer):
    grupos_de_verificacao = GrupoVerificacaoSerializer(many=True)

    class Meta:
        model = ModeloAteste
        fields = ('uuid', 'titulo', 'criado_em', 'grupos_de_verificacao')


class ModeloAtesteLookUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeloAteste
        fields = ('uuid', 'titulo', 'criado_em')


class ModeloAtesteSerializerCreate(serializers.ModelSerializer):
    grupos_de_verificacao = GrupoVerificacaoSerializer(many=True)
    itens_de_verificacao = ItensVerificacaoSerializer(many=True, required=False)

    def create(self, validated_data):
        grupos_de_verificacao_list = []
        grupos_de_verificacao = validated_data.pop('grupos_de_verificacao')
        modelo_ateste = ModeloAteste.objects.create(**validated_data)
        for grupo_verificacao in grupos_de_verificacao:
            itens_verificacao = grupo_verificacao.pop('itens_de_verificacao')
            grupo = GrupoVerificacao.objects.create(modelo=modelo_ateste, **dict(grupo_verificacao))
            grupos_de_verificacao_list.append(grupo)
            for item_verificacao in itens_verificacao:
                ItensVerificacao.objects.create(grupo=grupo, **dict(item_verificacao))

        modelo_ateste.grupos_de_verificacao.set(grupos_de_verificacao_list)
        return modelo_ateste

    class Meta:
        model = ModeloAteste
        fields = ('uuid', 'titulo', 'criado_em', 'grupos_de_verificacao', 'itens_de_verificacao')
