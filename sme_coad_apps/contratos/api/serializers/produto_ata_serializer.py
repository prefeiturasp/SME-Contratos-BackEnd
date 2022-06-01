from rest_framework import serializers

from ...api.serializers.produto_serializer import ProdutoSimplesSerializer
from ...models.ata import Ata, ProdutosAta
from ...models.produto import Produto


class ProdutoAtaSerializer(serializers.ModelSerializer):
    produto = ProdutoSimplesSerializer(required=False)

    class Meta:
        model = ProdutosAta
        fields = ('uuid', 'produto', 'quantidade_total', 'valor_unitario',
                  'valor_total', 'anexo')


class ProdutoAtaSerializerCreate(serializers.ModelSerializer):
    produto = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        queryset=Produto.objects.all()
    )
    ata = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        queryset=Ata.objects.all()
    )
    uuid = serializers.UUIDField(required=False)

    class Meta:
        model = ProdutosAta
        fields = ('id', 'uuid', 'produto', 'quantidade_total', 'valor_unitario', 'valor_total', 'ata', 'anexo')
