from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from ...services import gera_notificacoes_vigencia_contratos


class GeraNotificacoesVigenciaContratosViewSet(viewsets.ViewSet):

    def list(self, request):
        gera_notificacoes_vigencia_contratos()

        content = {
            'message': 'Solicitação recebida. As notificações de vigências de contrato serão geradas.',
        }
        return Response(content, status=status.HTTP_202_ACCEPTED)
