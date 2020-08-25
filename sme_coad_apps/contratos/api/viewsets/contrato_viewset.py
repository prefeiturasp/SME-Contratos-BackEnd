from django.db.models import Q
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from sme_coad_apps.contratos.models import ContratoUnidade
from sme_coad_apps.contratos.models.contrato import DocumentoFiscal
from ..serializers.contrato_serializer import ContratoSerializer, ContratoCreateSerializer, ContratoLookUpSerializer
from ...models import Contrato
from ....core.viewsets_abstracts import ComHistoricoViewSet


class ContratoViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    contratos_queryset = Contrato.objects.select_related(
        'empresa_contratada').select_related(
        'nucleo_responsavel').select_related(
        'gestor').select_related(
        'suplente').select_related(
        'tipo_servico').select_related(
        'edital').all()

    queryset = contratos_queryset

    serializer_class = ContratoSerializer

    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = (
        'situacao', 'tipo_servico', 'gestor', 'suplente', 'empresa_contratada', 'estado_contrato', 'termo_contrato')
    ordering_fields = ('data_ordem_inicio',)
    search_fields = ('processo',)

    def get_queryset(self):
        queryset = self.contratos_queryset

        encerramento_de = self.request.query_params.get('encerramento_de')
        encerramento_ate = self.request.query_params.get('encerramento_ate')
        if encerramento_de is not None and encerramento_ate is not None:
            queryset = queryset.filter(data_encerramento__range=[encerramento_de, encerramento_ate])

        equipamento = self.request.query_params.get('equipamento')

        if equipamento is not None:
            if equipamento == 'UE':
                queryset = queryset.filter(tem_ue=True)
            elif equipamento == 'CEU':
                queryset = queryset.filter(tem_ceu=True)
            elif equipamento == 'UA':
                queryset = queryset.filter(tem_ua=True)

        atribuido = self.request.query_params.get('atribuido')
        if atribuido is not None:
            queryset = queryset.filter(
                Q(gestor__nome__contains=atribuido.capitalize()) | Q(suplente__nome__contains=atribuido.capitalize()))

        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ContratoSerializer
        elif self.action == 'list':
            return ContratoSerializer
        else:
            return ContratoCreateSerializer

    @action(detail=False)
    def estados(self, _):
        return Response(Contrato.estados_to_json())

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
            DocumentoFiscal.objects.filter(contrato=contrato).delete()
            return Response(data={'detail': 'Contrato {} cancelado'.format(contrato.termo_contrato), 'status': 200})
        return Response(data=['Este contrato não pode ser cancelado'], status=status.HTTP_403_FORBIDDEN)
