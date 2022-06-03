from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response

from ....core.viewsets_abstracts import ComHistoricoReadOnlyViewSet, ComHistoricoViewSet
from ...models import Produto, UnidadeDeMedida
from ..serializers.produto_serializer import (
    ProdutoCreateSerializer,
    ProdutoLookUpSerializer,
    ProdutoSerializer,
    ProdutoSimplesSerializer,
    UnidadeDeMedidaSerializer
)
from ..utils.pagination import ProdutoPagination
from .filters import ProdutoFilter


class UnidadeDeMedidaViewSet(ComHistoricoReadOnlyViewSet):
    lookup_field = 'uuid'
    queryset = UnidadeDeMedida.objects.all()
    serializer_class = UnidadeDeMedidaSerializer

    @action(detail=False)
    def lookup(self, _):
        return Response(UnidadeDeMedidaSerializer(self.queryset.order_by('nome'), many=True).data)


class ProdutoViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    queryset = Produto.objects.all().order_by('-id')
    serializer_class = ProdutoSerializer
    pagination_class = ProdutoPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ProdutoFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProdutoSerializer
        elif self.action == 'list':
            return ProdutoLookUpSerializer
        else:
            return ProdutoCreateSerializer

    @action(detail=False)
    def simples(self, request):
        return Response(ProdutoSimplesSerializer(self.queryset.order_by('-id'), many=True).data)
