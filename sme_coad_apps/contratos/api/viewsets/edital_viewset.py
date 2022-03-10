from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response

from ....core.viewsets_abstracts import ComHistoricoViewSet
from ...api.serializers.edital_serializer import EditalLookUpSerializer, EditalSerializer, EditalSerializerCreate
from ...models.edital import Edital
from .filters import EditalFilter


class EditalViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    queryset = Edital.objects.all()
    serializer_class = EditalSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EditalFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EditalSerializer
        elif self.action == 'list':
            return EditalLookUpSerializer
        else:
            return EditalSerializerCreate

    @action(detail=False)
    def tipo_contratacao(self, _):
        return Response(Edital.tipo_contratacao_to_json())
