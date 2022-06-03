from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny

from ...models.ata import ProdutosAta
from ..serializers.produto_ata_serializer import ProdutoAtaSerializer


class ProdutoAtaViewSet(viewsets.ModelViewSet):
    serializer_class = ProdutoAtaSerializer
    queryset = ProdutosAta.objects.all()
    lookup_field = 'uuid'
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    search_fields = ('ata__uuid',)
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser, FormParser,)
