from rest_framework import serializers

from sme_coad_apps.core.helpers.update_instance_from_dict import update_instance_from_dict
from .grupo_verificacao_serializer import GrupoVerificacaoSerializer
from .intens_verificacao_serializer import ItensVerificacaoSerializer
from ..helpers.update_modelo_ateste import salvar_grupo
from ...models import ModeloAteste


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
        modelo = ModeloAteste.objects.create(**validated_data)
        for grupo_verificacao in grupos_de_verificacao:
            grupo = salvar_grupo(modelo, grupo_verificacao)
            grupos_de_verificacao_list.append(grupo)
        modelo.grupos_de_verificacao.set(grupos_de_verificacao_list)
        return modelo

    def update(self, instance, validated_data):
        grupos_de_verificacao_alterar_list = []
        grupos_de_verificacao = validated_data.pop('grupos_de_verificacao')
        instance.grupos_de_verificacao.all().delete()
        for grupo_verificacao in grupos_de_verificacao:
            grupo = salvar_grupo(instance, grupo_verificacao)
            grupos_de_verificacao_alterar_list.append(grupo)
        update_instance_from_dict(instance, validated_data)
        instance.grupos_de_verificacao.set(grupos_de_verificacao_alterar_list)
        instance.save()
        return instance

    class Meta:
        model = ModeloAteste
        fields = ('uuid', 'titulo', 'criado_em', 'grupos_de_verificacao', 'itens_de_verificacao')
