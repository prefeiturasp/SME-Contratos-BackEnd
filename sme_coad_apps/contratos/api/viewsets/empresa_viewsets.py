from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response

from ....core.viewsets_abstracts import ComHistoricoViewSet
from ...models.empresa import Empresa
from ..serializers.empresa_serializer import EmpresaCreateSerializer, EmpresaLookUpSerializer, EmpresaSerializer
from ..utils.pagination import EmpresaPagination
from .filters import EmpresaFilter


class EmpresaViewSet(ComHistoricoViewSet):
    lookup_field = 'uuid'
    queryset = Empresa.objects.all().order_by('-id')
    serializer_class = EmpresaSerializer
    pagination_class = EmpresaPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EmpresaFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EmpresaSerializer
        elif self.action == 'list':
            return EmpresaLookUpSerializer
        else:
            return EmpresaCreateSerializer

    @action(detail=False)
    def lookup(self, _):
        return Response(EmpresaLookUpSerializer(self.queryset.order_by('nome'), many=True).data)

    @action(detail=False)
    def lookup_completo(self, _):
        return Response(EmpresaSerializer(self.queryset.order_by('nome'), many=True).data)
