from ..serializers.contrato_serializer import ContratoSerializer

from ...models import Contrato
from ....core.viewsets_abstracts import ComHistoricoReadOnlyViewSet


class ContratoViewSet(ComHistoricoReadOnlyViewSet):
    lookup_field = 'uuid'
    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer
