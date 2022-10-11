from django_filters import rest_framework as filters
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from sme_coad_apps.contratos.models import ContratoUnidade
from sme_coad_apps.contratos.models.contrato import AnexoContrato

from ....core.viewsets_abstracts import ComHistoricoViewSet
from ...models import Contrato
from ..serializers.contrato_serializer import (
    ContratoCreateSerializer,
    ContratoLookUpSerializer,
    ContratoSerializer,
    ContratoSigpaeLookUpSerializer,
    ContratoSigpaeSerializer,
    ContratoSimplesSerializer
)
from ..utils.pagination import ContratoPagination
from .filters import ContratoFilter


class ContratoViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    contratos_queryset = Contrato.objects.select_related(
        'empresa_contratada').select_related(
        'nucleo_responsavel').select_related(
        'objeto').select_related(
        'edital').all()

    queryset = contratos_queryset
    serializer_class = ContratoSerializer
    pagination_class = ContratoPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ContratoFilter
    ordering_fields = ('data_ordem_inicio',)
    search_fields = ('processo',)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ContratoSerializer
        elif self.action == 'list':
            return ContratoSimplesSerializer
        else:
            return ContratoCreateSerializer

    @action(detail=False)
    def situacoes(self, _):
        return Response(Contrato.situacoes_to_json())

    @action(detail=False)
    def termos(self, _):
        return Response(ContratoLookUpSerializer(self.queryset.order_by('-alterado_em'), many=True).data)

    @action(detail=True, methods=['delete'], url_path='cancelar-cadastro-unico')
    def cancelar_cadastro_unico(self, request, uuid):
        contrato = self.get_object()
        if contrato.situacao == 'RASCUNHO':
            ContratoUnidade.objects.filter(contrato=contrato).delete()
            AnexoContrato.objects.filter(contrato=contrato).delete()
            return Response(data={'detail': f'Contrato {contrato.termo_contrato} cancelado', 'status': 200})
        return Response(data=['Este contrato não pode ser cancelado'], status=status.HTTP_403_FORBIDDEN)


class ContratoSigpaeViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'uuid'
    permission_classes = (IsAuthenticated,)
    queryset = Contrato.objects.all()
    serializer_class = ContratoSigpaeSerializer
    pagination_class = ContratoPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ContratoFilter

    @action(detail=False, url_path='termos-de-contratos')
    def lista_termos_de_contratos(self, _):
        return Response(ContratoSigpaeLookUpSerializer(self.queryset.order_by('-criado_em'), many=True).data)
