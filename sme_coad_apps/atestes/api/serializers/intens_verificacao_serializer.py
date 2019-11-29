from rest_framework import serializers

from ...models import ItensVerificacao, GrupoVerificacao


class ItensVerificacaoSerializer(serializers.ModelSerializer):
    grupo = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        queryset=GrupoVerificacao.objects.all()
    )

    class Meta:
        model = ItensVerificacao
        fields = ('uuid', 'item', 'descricao', 'grupo')
