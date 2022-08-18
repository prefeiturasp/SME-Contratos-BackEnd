from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response

from ....core.viewsets_abstracts import ComHistoricoViewSet
from ...api.serializers.aditamento_serializer import AditamentoCreateSerializer, AditamentoSerializer
from ...models.aditamento import Aditamento
from .filters import AditamentoFilter


class AditamentoViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    queryset = Aditamento.objects.all()
    serializer_class = AditamentoSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AditamentoFilter

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return AditamentoSerializer
        else:
            return AditamentoCreateSerializer

    @action(detail=False, url_path='objetos', methods=['get'])
    def lista_objetos_aditamentos(self, _):
        return Response(Aditamento.objetos_to_json())
