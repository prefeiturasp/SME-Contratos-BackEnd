from rest_framework import viewsets

from ..serializers.nucleo_serializer import NucleoSerializer
from ...models import Nucleo


class NucleoViewSet(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    queryset = Nucleo.objects.all()
    serializer_class = NucleoSerializer
