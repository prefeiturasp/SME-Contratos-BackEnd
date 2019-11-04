from rest_framework.decorators import action
from rest_framework.response import Response

from ..serializers.divisao_serializer import DivisaoSerializer, DivisaoSerializerCreator
from ..serializers.nucleo_serializer import NucleoSerializer
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

    @action(detail=True)
    def nucleos(self, request, uuid=None):
        divisao = self.get_object()
        nucleos = divisao.nucleo_set.all()

        serializer = NucleoSerializer(nucleos, many=True)
        return Response(serializer.data)
