from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from sme_coad_apps.core.api.serializers.historico_serializer import HistoricoSerializer


class ComHistoricoViewSet(viewsets.ModelViewSet):

    @action(detail=True)
    def historico(self, request, uuid):
        historico = self.get_object().historico.all()
        serializer = HistoricoSerializer(historico, many=True)
        return Response(serializer.data)

    class Meta:
        abstract = True
