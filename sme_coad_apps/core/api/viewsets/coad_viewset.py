from rest_framework.decorators import action
from rest_framework.response import Response

from ..serializers.coad_serializer import CoadSerializer, CoadCreateSerializer
from ...models.coad import Coad
from ...services import limpa_assessores_coad
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

    @action(detail=False, url_path='limpa-assessores')
    def limpa_assessores(self, _):
        limpa_assessores_coad()

        return Response({'message': 'Todos os assessores da COAD foram apagados'})
