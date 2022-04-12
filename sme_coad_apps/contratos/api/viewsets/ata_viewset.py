from rest_framework.permissions import IsAuthenticated

from ....core.viewsets_abstracts import ComHistoricoViewSet
from ...api.serializers.ata_serializer import AtaCreateSerializer, AtaLookUpSerializer, AtaSerializer
from ...models.ata import Ata
from ..utils.pagination import AtaPagination


class AtaViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    queryset = Ata.objects.all()
    serializer_class = AtaSerializer
    pagination_class = AtaPagination
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AtaSerializer
        elif self.action == 'list':
            return AtaLookUpSerializer
        else:
            return AtaCreateSerializer