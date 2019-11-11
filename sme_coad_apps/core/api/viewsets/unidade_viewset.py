from rest_framework import viewsets

from ..serializers.unidade_serializer import UnidadeSerializer
from ...models.unidade import Unidade


class UnidadeViewSet(viewsets.ModelViewSet):
    queryset = Unidade.objects.all().order_by('nome')
    serializer_class = UnidadeSerializer
