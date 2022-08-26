from django.urls import include, path
from rest_framework import routers

from .api.viewsets.aditamento_viewset import AditamentoViewSet
from .api.viewsets.anexo_contrato_viewset import AnexoContratoViewSet
from .api.viewsets.ata_viewset import AtaViewSet
from .api.viewsets.colunas_contrato_viewset import ColunasContratoViewSet
from .api.viewsets.contrato_unidade_viewset import ContratoUnidadeViewSet
from .api.viewsets.contrato_viewset import ContratoViewSet
from .api.viewsets.dotacao_valor_viewset import DotacaoOrcamentariaViewSet, DotacaoValorViewSet
from .api.viewsets.edital_viewset import EditalViewSet
from .api.viewsets.empresa_viewsets import EmpresaViewSet
from .api.viewsets.intercorrencia_viewset import ImpedimentoViewSet, RescisaoViewSet, SuspensaoViewSet
from .api.viewsets.notificacao_vigencia_contrato_viewsets import (
    GeraNotificacoesVigenciaContratosViewSet,
    MinhasNotificacoesVigenciaViewSet
)
from .api.viewsets.objeto_viewsets import ObjetoViewSet
from .api.viewsets.obricacao_contratual_viewset import ObrigacaoContratualViewSet
from .api.viewsets.produto_viewset import ProdutoViewSet, UnidadeDeMedidaViewSet

router = routers.DefaultRouter()

router.register('aditamentos', AditamentoViewSet)
router.register('atas', AtaViewSet)
router.register('colunas-contrato', ColunasContratoViewSet)
router.register('objetos', ObjetoViewSet)
router.register('empresas', EmpresaViewSet)
router.register('editais', EditalViewSet)
router.register('contratos', ContratoViewSet)
router.register('unidades-contratos', ContratoUnidadeViewSet)
router.register('anexos-contratos', AnexoContratoViewSet)
router.register('gera-notificacoes-vigencia-contratos', GeraNotificacoesVigenciaContratosViewSet,
                basename='gera-notificacoes-vigencia-contratos')
router.register('minhas-notificacoes-vigencia-contratos', MinhasNotificacoesVigenciaViewSet,
                basename='minhas-notificacoes-vigencia-contratos')
router.register('obrigacoes-contratuais', ObrigacaoContratualViewSet)
router.register('dotacoes-orcamentarias-valor', DotacaoValorViewSet)
router.register('dotacoes-orcamentarias', DotacaoOrcamentariaViewSet)
router.register('unidades-de-medida', UnidadeDeMedidaViewSet)
router.register('produtos', ProdutoViewSet)
router.register('intercorrencias/impedimento', ImpedimentoViewSet)
router.register('intercorrencias/rescisao', RescisaoViewSet)
router.register('intercorrencias/suspensao', SuspensaoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
