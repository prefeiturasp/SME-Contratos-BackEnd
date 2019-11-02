from ..serializers.divisao_serializer import DivisaoSerializer, DivisaoSerializerCreator

from ...models import Divisao
from ...viewsets_abstracts import ComHistoricoViewSet


class DivisaoViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    queryset = Divisao.objects.all()
    serializer_class = DivisaoSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DivisaoSerializer
        elif self.action == 'list':
            return DivisaoSerializer
        else:
            return DivisaoSerializerCreator
