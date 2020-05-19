from django.urls import path, include
from rest_framework import routers

from .api.viewsets.colunas_contrato_viewset import ColunasContratoViewSet
from .api.viewsets.contrato_unidade_viewset import ContratoUnidadeViewSet
from .api.viewsets.contrato_viewset import ContratoViewSet
from .api.viewsets.obricacao_contratual_viewset import ObrigacaoContratualViewSet
from .api.viewsets.documento_fiscal_viewset import DocumentoFiscalViewSet
from .api.viewsets.empresa_viewsets import EmpresaViewSet
from .api.viewsets.notificacao_vigencia_contrato_viewsets import GeraNotificacoesVigenciaContratosViewSet
from .api.viewsets.notificacao_vigencia_contrato_viewsets import MinhasNotificacoesVigenciaViewSet
from .api.viewsets.tipo_servico_viewsets import TipoServicoViewSet
from .api.viewsets.dotacao_valor_viewset import DotacaoValorViewSet

router = routers.DefaultRouter()

router.register('colunas-contrato', ColunasContratoViewSet)
router.register('tipos-servico', TipoServicoViewSet)
router.register('empresas', EmpresaViewSet)
router.register('contratos', ContratoViewSet)
router.register('unidades-contratos', ContratoUnidadeViewSet)
router.register('documentos-fiscais', DocumentoFiscalViewSet)
router.register('gera-notificacoes-vigencia-contratos', GeraNotificacoesVigenciaContratosViewSet,
                basename='gera-notificacoes-vigencia-contratos')
router.register('minhas-notificacoes-vigencia-contratos', MinhasNotificacoesVigenciaViewSet,
                basename='minhas-notificacoes-vigencia-contratos')
router.register('obrigacoes-contratuais', ObrigacaoContratualViewSet)
router.register('dotacao-orcamentaria', DotacaoValorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
