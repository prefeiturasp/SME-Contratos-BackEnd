from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from ....core.viewsets_abstracts import ComHistoricoViewSet
from ...models.obrigacao_contratual import ObrigacaoContratual
from ..serializers.obrigacao_contratual_serializer import (
    ObrigacaoContratualCreatorSerializer,
    ObrigacaoContratualSerializer
)


class ObrigacaoContratualViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    queryset = ObrigacaoContratual.objects.all()
    serializer_class = ObrigacaoContratualSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    filter_fields = ('contrato__uuid',)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ObrigacaoContratualSerializer
        elif self.action == 'list':
            return ObrigacaoContratualSerializer
        else:
            return ObrigacaoContratualCreatorSerializer
