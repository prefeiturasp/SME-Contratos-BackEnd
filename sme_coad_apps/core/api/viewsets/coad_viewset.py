from ..serializers.coad_serializer import CoadSerializer, CoadCreateSerializer

from ...models.coad import Coad
from ...viewsets_abstracts import ComHistoricoViewSet


class CoadViewSet(ComHistoricoViewSet):
    queryset = Coad.objects.all()
    serializer_class = CoadSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CoadSerializer
        elif self.action == 'list':
            return CoadSerializer
        else:
            return CoadCreateSerializer
