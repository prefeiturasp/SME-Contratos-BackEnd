from rest_framework.decorators import action
from rest_framework.response import Response

from ..serializers.nucleo_serializer import NucleoSerializer, NucleoLookUpSerializer
from ...models import Nucleo
from ...viewsets_abstracts import ComHistoricoViewSet


class NucleoViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    queryset = Nucleo.objects.select_related('divisao').all()
    serializer_class = NucleoSerializer

    @action(detail=False)
    def lookup(self, _):
        return Response(NucleoLookUpSerializer(self.queryset, many=True).data)
