from ..serializers.nucleo_serializer import NucleoSerializer
from ...models import Nucleo
from ...viewsets_abstracts import ComHistoricoViewSet


class NucleoViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    queryset = Nucleo.objects.all()
    serializer_class = NucleoSerializer
