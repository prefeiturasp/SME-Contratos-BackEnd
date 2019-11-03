from rest_framework import viewsets
from rest_framework.response import Response

from ..serializers.contrato_unidade_serializer import ContratoUnidadeSerializer
from ...api.utils.contrato_unidade_utils import convert_contrato_unidade_to_json
from ...models.contrato import ContratoUnidade


class ContratoUnidadeViewSet(viewsets.ModelViewSet):
    serializer_class = ContratoUnidadeSerializer
    queryset = ContratoUnidade.objects.all()
    lookup_field = 'contrato__uuid'

    def list(self, request):
        return Response(data=[])

    def retrieve(self, request, *args, **kwargs):
        uuid = kwargs['contrato__uuid']
        unidades = ContratoUnidade.objects.filter(contrato__uuid=uuid)
        unidades_contrato_json = convert_contrato_unidade_to_json(unidades)
        return Response(data=unidades_contrato_json)
