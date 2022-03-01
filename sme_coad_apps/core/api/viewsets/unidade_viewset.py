from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ...models.unidade import Unidade
from ..serializers.unidade_serializer import UnidadeLookUpSerializer, UnidadeSerializer


class UnidadeViewSet(viewsets.ModelViewSet):
    queryset = Unidade.objects.all().order_by('nome')
    serializer_class = UnidadeSerializer

    @action(detail=False)
    def lookup(self, _):
        return Response(UnidadeLookUpSerializer(self.queryset.order_by('nome'), many=True).data)
