from rest_framework.decorators import action
from rest_framework.response import Response

from ..serializers.nucleo_serializer import NucleoSerializer, NucleoLookUpSerializer, NucleoCreateSerializer
from ...models import Nucleo
from ...viewsets_abstracts import ComHistoricoViewSet


class NucleoViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    queryset = Nucleo.objects.select_related('divisao').all()
    serializer_class = NucleoSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return NucleoSerializer
        elif self.action == 'list':
            return NucleoSerializer
        else:
            return NucleoCreateSerializer

    @action(detail=False)
    def lookup(self, _):
        return Response(NucleoLookUpSerializer(self.queryset, many=True).data)
