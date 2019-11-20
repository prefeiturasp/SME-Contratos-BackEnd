from ..serializers.obrigacao_contratual_serializer import ObrigacaoContratualSerializer
from ...models.obrigacao_contratual import ObrigacaoContratual
from ....core.viewsets_abstracts import ComHistoricoViewSet


class ObrigacaoContratualViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    queryset = ObrigacaoContratual.objects.all()
    serializer_class = ObrigacaoContratualSerializer

    def get_queryset(self):
        queryset = self.queryset
        contrato = self.request.query_params.get('contratoUuid')
        if contrato is not None:
            queryset = queryset.filter(contrato__uuid='contrato')

        return queryset
