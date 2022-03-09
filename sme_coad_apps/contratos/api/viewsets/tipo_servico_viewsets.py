from rest_framework.decorators import action
from rest_framework.response import Response

from ....core.viewsets_abstracts import ComHistoricoViewSet
from ...models.tipo_servico import TipoServico
from ..serializers.tipo_servico_serializer import (
    TipoServicoCreateSerializer,
    TipoServicoLookupSerializer,
    TipoServicoSerializer
)


class TipoServicoViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    queryset = TipoServico.objects.all()
    serializer_class = TipoServicoSerializer
    http_method_names = ['get', 'post']

    def get_serializer_class(self):
        if self.action == 'create':
            return TipoServicoCreateSerializer
        else:
            return TipoServicoSerializer

    @action(detail=False)
    def lookup(self, _):
        return Response(TipoServicoLookupSerializer(self.queryset.order_by('nome'), many=True).data)
