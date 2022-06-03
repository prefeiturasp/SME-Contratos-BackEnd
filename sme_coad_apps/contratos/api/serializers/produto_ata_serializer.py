import environ
from rest_framework import serializers

from ...api.serializers.produto_serializer import ProdutoSimplesSerializer
from ...models.ata import Ata, ProdutosAta
from ...models.produto import Produto

env = environ.Env()
API_URL = f'{env("API_URL")}'


class ProdutoAtaSerializer(serializers.ModelSerializer):
    produto = ProdutoSimplesSerializer(required=False)
    anexo = serializers.SerializerMethodField('get_anexo')

    def get_anexo(self, obj):
        if bool(obj.anexo):
            return '%s%s' % (API_URL, obj.anexo.url)
        else:
            return None

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
    anexo = serializers.CharField()

    class Meta:
        model = ProdutosAta
        fields = ('id', 'uuid', 'produto', 'quantidade_total', 'valor_unitario', 'valor_total', 'ata', 'anexo')
