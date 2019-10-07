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

    def get_queryset(self):
        contratos = Contrato.objects \
            .select_related('empresa_contratada') \
            .select_related('nucleo_responsavel') \
            .select_related('gestor') \
            .select_related() \
            .all()

        queryset = contratos

        encerramento_de = self.request.query_params.get('encerramento_de')
        encerramento_ate = self.request.query_params.get('encerramento_ate')

        if encerramento_de is not None and encerramento_ate is not None:
            queryset = queryset.filter(data_encerramento__range=[encerramento_de, encerramento_ate])

        return queryset
