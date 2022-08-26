from rest_framework.decorators import action
from rest_framework.response import Response

from ....core.viewsets_abstracts import ComHistoricoViewSet
from ...api.serializers.intercorrencia_serializer import (
    RescisaoCreateSerializer,
    RescisaoSerializer,
    SuspensaoCreateSerializer,
    SuspensaoSerializer
)
from ...models.intercorrencia import Rescisao, Suspensao


class RescisaoViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    queryset = Rescisao.objects.all()
    serializer_class = RescisaoSerializer

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return RescisaoSerializer
        else:
            return RescisaoCreateSerializer

    @action(detail=False, url_path='motivos-rescisao', methods=['get'])
    def lista_motivos_rescisao_intercorrencias(self, _):
        return Response(Rescisao.motivos_rescisao_to_json())


class SuspensaoViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    queryset = Suspensao.objects.all()
    serializer_class = SuspensaoSerializer

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return SuspensaoSerializer
        else:
            return SuspensaoCreateSerializer

    @action(detail=False, url_path='motivos-suspensao', methods=['get'])
    def lista_motivos_suspensao_intercorrencias(self, _):
        return Response(Suspensao.motivos_suspensao_to_json())
