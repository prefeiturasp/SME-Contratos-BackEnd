from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response

from ....core.viewsets_abstracts import ComHistoricoViewSet
from ...api.serializers.edital_serializer import (
    EditalLookUpSerializer,
    EditalSerializer,
    EditalSerializerCreate,
    EditalSimplesSerializer
)
from ...models.edital import Edital
from ..utils.pagination import EditalPagination
from .filters import EditalFilter


class EditalViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    queryset = Edital.objects.all()
    serializer_class = EditalSerializer
    pagination_class = EditalPagination
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

    @action(detail=False)
    def lista(self, _):
        return Response(EditalSimplesSerializer(self.queryset.order_by('-id'), many=True).data)
