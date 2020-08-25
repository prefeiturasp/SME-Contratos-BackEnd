from ..serializers.dotacao_valor_serializer import (DotacaoValorSerializer,
                                                    DotacaoValorCreatorSerializer)
from ...models.dotacao_valor import DotacaoValor
from ....core.viewsets_abstracts import ComHistoricoViewSet
from rest_framework.filters import SearchFilter
from django_filters import rest_framework as filters


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
