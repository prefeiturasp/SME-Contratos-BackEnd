from rest_framework import status, viewsets
from rest_framework.response import Response

from ...models.notificacao_vigencia_contrato import NotificacaoVigenciaContrato


class GeraNotificacoesVigenciaContratosViewSet(viewsets.ViewSet):

    def list(self, request):
        NotificacaoVigenciaContrato.gera_notificacoes()

        content = {
            'message': 'Solicitação recebida. As notificações de vigências de contrato serão geradas.',
        }
        return Response(content, status=status.HTTP_202_ACCEPTED)


class MinhasNotificacoesVigenciaViewSet(viewsets.ViewSet):

    def list(self, request):
        qtd_notificacoes = NotificacaoVigenciaContrato.get_notificacoes_do_usuario(self.request.user).count()

        content = {
            'contratos_vencendo': qtd_notificacoes,
        }
        return Response(content, status=status.HTTP_200_OK)
