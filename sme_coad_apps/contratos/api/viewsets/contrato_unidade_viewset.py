from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from ...models.contrato import ContratoUnidade
from ..serializers.contrato_unidade_serializer import (
    ContratoUnidadeCreatorSerializer,
    ContratoUnidadeLookUpSerializer,
    ContratoUnidadeSerializer
)


class ContratoUnidadeViewSet(viewsets.ModelViewSet):
    serializer_class = ContratoUnidadeSerializer
    queryset = ContratoUnidade.objects.all()
    lookup_field = 'uuid'
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    filter_fields = ('contrato__uuid',)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ContratoUnidadeLookUpSerializer
        elif self.action == 'list':
            return ContratoUnidadeLookUpSerializer
        else:
            return ContratoUnidadeCreatorSerializer
