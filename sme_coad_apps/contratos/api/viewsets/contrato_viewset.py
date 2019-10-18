from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from ..serializers.contrato_serializer import ContratoSerializer
from ...models import Contrato, ContratoUnidade
from ....core.viewsets_abstracts import ComHistoricoReadOnlyViewSet


class ContratoViewSet(ComHistoricoReadOnlyViewSet):
    lookup_field = 'uuid'
    contratos_queryset = Contrato.objects.select_related(
        'empresa_contratada').select_related(
        'nucleo_responsavel').select_related(
        'gestor').select_related(
        'tipo_servico').select_related().all()

    queryset = contratos_queryset

    serializer_class = ContratoSerializer

    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('situacao', 'tipo_servico', 'gestor', 'empresa_contratada', 'estado_contrato', 'termo_contrato')
    ordering_fields = ('data_ordem_inicio',)
    search_fields = ('processo',)

    def get_queryset(self):
        # c_ua = Contrato.objects.filter(id__in=[linha.contrato.id for linha in ContratoUnidade.objects.filter(unidade__equipamento='CEU')])
        queryset = self.contratos_queryset

        encerramento_de = self.request.query_params.get('encerramento_de')
        encerramento_ate = self.request.query_params.get('encerramento_ate')
        if encerramento_de is not None and encerramento_ate is not None:
            queryset = queryset.filter(data_encerramento__range=[encerramento_de, encerramento_ate])

        equipamento = self.request.query_params.get('equipamento')
        contratos_por_equipamento = [linha.contrato.id for linha in
                                               ContratoUnidade.objects.filter(unidade__equipamento=equipamento)]
        if equipamento is not None:
            queryset = queryset.prefetch_related('unidades')
            queryset = queryset.filter(id__in=contratos_por_equipamento)

        return queryset

    @action(detail=False)
    def estados(self, _):
        return Response(Contrato.estados_to_json())

    @action(detail=False)
    def situacoes(self, _):
        return Response(Contrato.situacoes_to_json())
