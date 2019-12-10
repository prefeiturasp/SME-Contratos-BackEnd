from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny

from ..serializers.documento_fiscal_serializer import DocumentoFiscalSerializer
from ...models.contrato import DocumentoFiscal


class DocumentoFiscalViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentoFiscalSerializer
    queryset = DocumentoFiscal.objects.all()
    lookup_field = 'uuid'
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    search_fields = ('contrato__uuid',)
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser, FormParser,)
