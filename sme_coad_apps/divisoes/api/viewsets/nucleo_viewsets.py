from rest_framework import viewsets

from ..serializers.nucleo_serializer import NucleoSerializer
from ....divisoes.models.nucleo import Nucleo


class NucleoViewSet(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    queryset = Nucleo.objects.all()
    serializer_class = NucleoSerializer
