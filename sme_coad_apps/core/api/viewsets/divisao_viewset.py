from ..serializers.divisao_serializer import DivisaoSerializer

from ...models import Divisao
from ...viewsets_abstracts import ComHistoricoViewSet


class DivisaoViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    queryset = Divisao.objects.all()
    serializer_class = DivisaoSerializer
