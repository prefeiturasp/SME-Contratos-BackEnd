from ....core.viewsets_abstracts import ComHistoricoViewSet
from ...api.serializers.edital_serializer import EditalLookUpSerializer, EditalSerializer, EditalSerializerCreate
from ...models.edital import Edital
from ..utils.pagination import EditalPagination


class EditalViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    queryset = Edital.objects.all()
    serializer_class = EditalSerializer
    pagination_class = EditalPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EditalSerializer
        elif self.action == 'list':
            return EditalLookUpSerializer
        else:
            return EditalSerializerCreate
