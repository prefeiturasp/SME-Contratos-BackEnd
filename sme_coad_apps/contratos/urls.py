from django.urls import path, include
from rest_framework import routers

from .api.viewsets.contrato_viewset import ContratoViewSet
from .api.viewsets.tipo_servico_viewsets import TipoServicoViewSet

router = routers.DefaultRouter()

router.register('tipos-servico', TipoServicoViewSet)
router.register('contratos', ContratoViewSet)

urlpatterns = [
    path('', include(router.urls))
]
