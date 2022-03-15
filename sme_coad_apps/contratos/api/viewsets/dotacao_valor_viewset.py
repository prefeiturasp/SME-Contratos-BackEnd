from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from ....core.viewsets_abstracts import ComHistoricoViewSet
from ...models.dotacao_valor import DotacaoValor
from ..serializers.dotacao_valor_serializer import DotacaoValorCreatorSerializer, DotacaoValorSerializer


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
