from rest_framework import viewsets

from ...models import Divisao
from ..serializers.divisao_serializer import DivisaoSerializer


class DivisaoViewSet(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    queryset = Divisao.objects.all()
    serializer_class = DivisaoSerializer
