from django.urls import path, include
from rest_framework import routers

from .api.viewsets.contrato_unidade_viewset import ContratoUnidadeViewSet
from .api.viewsets.contrato_viewset import ContratoViewSet
from .api.viewsets.empresa_viewsets import EmpresaViewSet
from .api.viewsets.tipo_servico_viewsets import TipoServicoViewSet
from .api.viewsets.colunas_contrato_viewset import ColunasContratoViewSet

router = routers.DefaultRouter()

router.register('colunas-contrato', ColunasContratoViewSet)
router.register('tipos-servico', TipoServicoViewSet)
router.register('empresas', EmpresaViewSet)
router.register('contratos', ContratoViewSet)
router.register('unidades-contratos', ContratoUnidadeViewSet)

urlpatterns = [
    path('', include(router.urls))
]
