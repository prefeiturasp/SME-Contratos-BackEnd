from rest_framework.decorators import action
from rest_framework.response import Response

from ....core.viewsets_abstracts import ComHistoricoReadOnlyViewSet
from ...models.tipo_servico import TipoServico
from ..serializers.tipo_servico_serializer import TipoServicoLookupSerializer, TipoServicoSerializer


class TipoServicoViewSet(ComHistoricoReadOnlyViewSet):
    lookup_field = 'uuid'
    queryset = TipoServico.objects.all()
    serializer_class = TipoServicoSerializer

    @action(detail=False)
    def lookup(self, _):
        return Response(TipoServicoLookupSerializer(self.queryset.order_by('nome'), many=True).data)
