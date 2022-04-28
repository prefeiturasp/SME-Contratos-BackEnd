from rest_framework.decorators import action
from rest_framework.response import Response

from ....core.viewsets_abstracts import ComHistoricoReadOnlyViewSet, ComHistoricoViewSet
from ...models import Produto, UnidadeDeMedida
from ..serializers.produto_serializer import ProdutoCreateSerializer, ProdutoSerializer, UnidadeDeMedidaSerializer


class UnidadeDeMedidaViewSet(ComHistoricoReadOnlyViewSet):
    lookup_field = 'uuid'
    queryset = UnidadeDeMedida.objects.all()
    serializer_class = UnidadeDeMedidaSerializer

    @action(detail=False)
    def lookup(self, _):
        return Response(UnidadeDeMedidaSerializer(self.queryset.order_by('nome'), many=True).data)


class ProdutoViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return ProdutoSerializer
        else:
            return ProdutoCreateSerializer
