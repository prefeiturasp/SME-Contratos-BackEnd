from ..serializers.obrigacao_contratual_serializer import (ObrigacaoContratualSerializer,
                                                           ObrigacaoContratualCreatorSerializer)
from ...models.obrigacao_contratual import ObrigacaoContratual
from ....core.viewsets_abstracts import ComHistoricoViewSet
from rest_framework.filters import SearchFilter
from django_filters import rest_framework as filters


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
