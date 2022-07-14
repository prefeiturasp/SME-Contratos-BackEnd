from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny

from ...models.contrato import AnexoContrato
from ..serializers.anexo_contrato_serializer import AnexoContratolSerializer, AnexoContratolSerializerCreate


class AnexoContratoViewSet(viewsets.ModelViewSet):
    serializer_class = AnexoContratolSerializer
    queryset = AnexoContrato.objects.all()
    lookup_field = 'uuid'
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    search_fields = ('contrato__uuid',)
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser, FormParser,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AnexoContratolSerializer
        elif self.action == 'list':
            return AnexoContratolSerializer
        else:
            return AnexoContratolSerializerCreate
