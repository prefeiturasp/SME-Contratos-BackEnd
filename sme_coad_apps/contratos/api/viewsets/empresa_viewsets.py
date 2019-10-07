from rest_framework.decorators import action
from rest_framework.response import Response

from ..serializers.empresa_serializer import EmpresaLookUpSerializer, EmpresaSerializer
from ...models.empresa import Empresa
from ....core.viewsets_abstracts import ComHistoricoReadOnlyViewSet


class EmpresaViewSet(ComHistoricoReadOnlyViewSet):
    lookup_field = 'uuid'
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

    @action(detail=False)
    def lookup(self, _):
        return Response(EmpresaLookUpSerializer(self.queryset, many=True).data)
