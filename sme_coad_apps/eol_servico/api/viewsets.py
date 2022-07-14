from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from sme_coad_apps.eol_servico.services import EOLException, EOLService


class EquipamentosEOLViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        codigo_subprefeitura = request.query_params.get('codigo_subprefeitura', None)
        codigo_dre = request.query_params.get('codigo_dre', None)
        tipo_escola = request.query_params.get('tipo_escola', None)
        tipo_unidade = request.query_params.get('tipo_unidade', None)
        nome_unidade = request.query_params.get('nome_unidade', None)
        codigo_eol_unidade = request.query_params.get('codigo_eol_unidade', None)
        if tipo_unidade:
            tipo_unidade = tipo_unidade.split(',')
        if tipo_escola:
            tipo_escola = tipo_escola.split(',')

        try:
            response = EOLService.buscar_equipamentos(codigo_subprefeitura=codigo_subprefeitura, codigo_dre=codigo_dre,
                                                      tipo_escola=tipo_escola, tipo_unidade=tipo_unidade,
                                                      nome_unidade=nome_unidade, codigo_eol_unidade=codigo_eol_unidade)
            return Response(response)
        except EOLException as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
