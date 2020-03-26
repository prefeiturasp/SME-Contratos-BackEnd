from ..serializers.colunas_contrato_serializer import ColunasContratoSerializer
from ...models.colunas_contrato import ColunasContrato
from ....core.viewsets_abstracts import ComHistoricoViewSet


class ColunasContratoViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    queryset = ColunasContrato.objects.all()
    serializer_class = ColunasContratoSerializer

    def get_queryset(self):
        return ColunasContrato.objects.filter(usuario=self.request.user)
