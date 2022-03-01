from rest_framework import serializers

from ...models import GrupoVerificacao, ItensVerificacao


class ItensVerificacaoSerializer(serializers.ModelSerializer):
    grupo = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        queryset=GrupoVerificacao.objects.all()
    )

    class Meta:
        model = ItensVerificacao
        fields = ('uuid', 'item', 'descricao', 'grupo')


class ItensVerificacaoSerializeCreate(serializers.ModelSerializer):
    grupo = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        queryset=GrupoVerificacao.objects.all()
    )

    def create(self, validated_data):
        item = ItensVerificacao.objects.create(**validated_data)
        return item

    class Meta:
        model = ItensVerificacao
        fields = ('uuid', 'item', 'descricao', 'grupo')
