from rest_framework.decorators import action
from rest_framework.response import Response

from ....core.viewsets_abstracts import ComHistoricoReadOnlyViewSet
from ...models.empresa import Empresa
from ..serializers.empresa_serializer import EmpresaLookUpSerializer, EmpresaSerializer


class EmpresaViewSet(ComHistoricoReadOnlyViewSet):
    lookup_field = 'uuid'
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

    @action(detail=False)
    def lookup(self, _):
        return Response(EmpresaLookUpSerializer(self.queryset.order_by('nome'), many=True).data)
