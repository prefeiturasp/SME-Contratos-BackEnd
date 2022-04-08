from rest_framework.permissions import IsAuthenticated

from ....core.viewsets_abstracts import ComHistoricoViewSet
from ...api.serializers.ata_serializer import AtaCreateSerializer, AtaSerializer
from ...models.ata import Ata


class AtaViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    queryset = Ata.objects.all()
    serializer_class = AtaSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AtaSerializer
        elif self.action == 'list':
            return AtaSerializer
        else:
            return AtaCreateSerializer
