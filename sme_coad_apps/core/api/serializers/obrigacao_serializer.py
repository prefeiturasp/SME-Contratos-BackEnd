from rest_framework import serializers

from ...models import ItemObrigacao, GrupoObrigacao


class ItemObrigacaoSerializer(serializers.ModelSerializer):
    grupo = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        queryset=GrupoObrigacao.objects.all()
    )

    class Meta:
        model = ItemObrigacao
        fields = ('uuid', 'item', 'descricao', 'grupo')


class ItemObrigacaoSerializeCreate(serializers.ModelSerializer):
    grupo = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        queryset=GrupoObrigacao.objects.all()
    )

    def create(self, validated_data):
        item = ItemObrigacao.objects.create(**validated_data)
        return item

    class Meta:
        model = ItemObrigacao
        fields = ('uuid', 'item', 'descricao', 'grupo')
