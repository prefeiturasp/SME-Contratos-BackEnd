from rest_framework import serializers

from sme_coad_apps.core.helpers.update_instance_from_dict import update_instance_from_dict

from ...api.utils.edital_utils import salvar_itens_de_grupo
from ...models.edital import Edital
from .grupo_obrigacao_serializer import GrupoObrigacaoSerializer
from .obrigacao_serializer import ObrigacaoSerializer


class EditalSerializer(serializers.ModelSerializer):
    grupos_de_obrigacao = serializers.SerializerMethodField()

    class Meta:
        model = Edital
        fields = ('uuid', 'numero', 'criado_em', 'grupos_de_obrigacao')

    def get_grupos_de_obrigacao(self, instance):
        grupo = instance.grupos_de_obrigacao.all().order_by('id')
        return GrupoObrigacaoSerializer(grupo, many=True).data


class EditalLookUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edital
        fields = ('uuid', 'numero', 'criado_em')


class EditalSerializerCreate(serializers.ModelSerializer):
    grupos_de_obrigacao = GrupoObrigacaoSerializer(many=True, required=False)
    itens_de_obrigacao = ObrigacaoSerializer(many=True, required=False)

    def create(self, validated_data):
        grupos_de_obrigacao_list = []
        grupos_de_obrigacao = validated_data.pop('grupos_de_obrigacao', [])
        edital = Edital.objects.create(**validated_data)
        for grupo_obrigacao in grupos_de_obrigacao:
            grupo = salvar_itens_de_grupo(edital, grupo_obrigacao)
            grupos_de_obrigacao_list.append(grupo)
        edital.grupos_de_obrigacao.set(grupos_de_obrigacao_list)
        return edital

    def update(self, instance, validated_data):
        grupos_de_obrigacao_alterar_list = []
        grupos_de_obrigacao = validated_data.pop('grupos_de_obrigacao')
        instance.grupos_de_obrigacao.all().delete()
        for grupo_obrigacao in grupos_de_obrigacao:
            grupo = salvar_itens_de_grupo(instance, grupo_obrigacao)
            grupos_de_obrigacao_alterar_list.append(grupo)
        update_instance_from_dict(instance, validated_data)
        instance.grupos_de_obrigacao.set(grupos_de_obrigacao_alterar_list)
        instance.save()
        return instance

    class Meta:
        model = Edital
        fields = ('uuid', 'numero', 'criado_em', 'grupos_de_obrigacao', 'itens_de_obrigacao')
