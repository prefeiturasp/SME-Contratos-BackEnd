from ..serializers.edital_serializer import (EditalSerializer, EditalLookUpSerializer, EditalSerializerCreate)
from ...models.edital import Edital
from ....core.viewsets_abstracts import ComHistoricoViewSet


class EditalViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    queryset = Edital.objects.all()
    serializer_class = EditalSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EditalSerializer
        elif self.action == 'list':
            return EditalLookUpSerializer
        else:
            return EditalSerializerCreate
