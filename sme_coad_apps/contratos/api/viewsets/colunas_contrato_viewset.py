from rest_framework.decorators import action
from rest_framework.response import Response

from ..serializers.colunas_contrato_serializer import ColunasContratoSerializer
from ...models.colunas_contrato import ColunasContrato
from ....core.viewsets_abstracts import ComHistoricoViewSet

class ColunasContratoViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    queryset = ColunasContrato.objects.all()
    serializer_class = ColunasContratoSerializer

    # @action(detail=False)
    # def lookup(self, _):
    #     return
