from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter

from ..serializers.contrato_serializer import ContratoSerializer
from ...models import Contrato
from ....core.viewsets_abstracts import ComHistoricoReadOnlyViewSet


class ContratoViewSet(ComHistoricoReadOnlyViewSet):
    lookup_field = 'uuid'
    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer

    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('situacao', 'tipo_servico', 'gestor', 'empresa_contratada', 'estado_contrato', 'termo_contrato')
    ordering_fields = ('data_ordem_inicio',)
    search_fields = ('processo',)
