from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from sme_coad_apps.contratos.api.utils.pagination import DotacaoOrcamentariaPagination

from ....core.viewsets_abstracts import ComHistoricoViewSet
from ...models.dotacao_valor import DotacaoOrcamentaria, DotacaoValor
from ..serializers.dotacao_valor_serializer import (
    DotacaoOrcamentariaCreatorSerializer,
    DotacaoOrcamentariaSerializer,
    DotacaoValorCreatorSerializer,
    DotacaoValorSerializer
)


class DotacaoValorViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    queryset = DotacaoValor.objects.all()
    serializer_class = DotacaoValorSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    filter_fields = ('contrato__uuid',)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DotacaoValorSerializer
        elif self.action == 'list':
            return DotacaoValorSerializer
        else:
            return DotacaoValorCreatorSerializer


class DotacaoOrcamentariaViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    permission_classes = [IsAuthenticated]
    queryset = DotacaoOrcamentaria.objects.all()
    serializer_class = DotacaoOrcamentariaSerializer
    pagination_class = DotacaoOrcamentariaPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DotacaoOrcamentariaSerializer
        elif self.action == 'list':
            return DotacaoOrcamentariaSerializer
        else:
            return DotacaoOrcamentariaCreatorSerializer
