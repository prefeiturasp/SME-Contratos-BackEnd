from rest_framework import viewsets
from rest_framework.response import Response

from sme_coad_apps.contratos.api.utils.contrato_unidade_utils import convert_contrato_unidade_to_json
from ..serializers.contrato_unidade_serializer import (ContratoUnidadeSerializer,
                                                       ContratoUnidadeLookUpSerializer,
                                                       ContratoUnidadeCreatorSerializer)
from ...models.contrato import ContratoUnidade


class ContratoUnidadeViewSet(viewsets.ModelViewSet):
    serializer_class = ContratoUnidadeSerializer
    queryset = ContratoUnidade.objects.all()
    lookup_field = 'contrato__uuid'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ContratoUnidadeLookUpSerializer
        elif self.action == 'list':
            return ContratoUnidadeSerializer
        else:
            return ContratoUnidadeCreatorSerializer

    def list(self, request, contrato=None):
        return Response(data=[])

    def retrieve(self, request, **kwargs):
        uuid = kwargs['contrato__uuid']
        unidades = ContratoUnidade.objects.filter(contrato__uuid=uuid)
        unidades_contrato_json = convert_contrato_unidade_to_json(unidades)
        return Response(data=unidades_contrato_json)
