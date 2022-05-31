from rest_framework import serializers

from ...models.ata import Ata, ProdutosAta
from ...models.produto import Produto
from ...api.serializers.produto_serializer import ProdutoSimplesSerializer


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

    class Meta:
        model = ProdutosAta
        exclude = ('id',)
