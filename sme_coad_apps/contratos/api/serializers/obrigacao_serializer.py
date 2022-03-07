from rest_framework import serializers

from ...models.obrigacao import GrupoObrigacao, Obrigacao


class ObrigacaoSerializer(serializers.ModelSerializer):
    grupo = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        queryset=GrupoObrigacao.objects.all()
    )

    class Meta:
        model = Obrigacao
        fields = ('uuid', 'item', 'descricao', 'grupo')


class ObrigacaoSerializeCreate(serializers.ModelSerializer):
    grupo = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        queryset=GrupoObrigacao.objects.all()
    )

    def create(self, validated_data):
        item = Obrigacao.objects.create(**validated_data)
        return item

    class Meta:
        model = Obrigacao
        fields = ('uuid', 'item', 'descricao', 'grupo')
