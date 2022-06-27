from rest_framework.decorators import action
from rest_framework.response import Response

from ....core.viewsets_abstracts import ComHistoricoViewSet
from ...models.objeto import Objeto
from ..serializers.objeto_serializer import ObjetoCreateSerializer, ObjetoLookupSerializer, ObjetoSerializer


class ObjetoViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    queryset = Objeto.objects.all()
    serializer_class = ObjetoSerializer
    http_method_names = ['get', 'post']

    def get_serializer_class(self):
        if self.action == 'create':
            return ObjetoCreateSerializer
        else:
            return ObjetoSerializer

    @action(detail=False)
    def lookup(self, _):
        return Response(ObjetoLookupSerializer(self.queryset.order_by('nome'), many=True).data)
