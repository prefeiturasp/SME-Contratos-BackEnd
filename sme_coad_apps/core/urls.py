from django.urls import include, path
from rest_framework import routers

from sme_coad_apps.atestes.urls import router as atestes_router
from sme_coad_apps.contratos.urls import router as contratos_router
from sme_coad_apps.users.urls import router as usuarios_router

from ..contratos.models.contrato import SafiToken
from ..core.api.viewsets.edital_viewset import EditalViewSet
from ..core.api.viewsets.unidade_viewset import UnidadeViewSet
from .api.viewsets.coad_assessor_viewset import CoadAssessorViewSet
from .api.viewsets.coad_viewset import CoadViewSet
from .api.viewsets.divisao_viewset import DivisaoViewSet
from .api.viewsets.nucleo_viewsets import NucleoViewSet

router = routers.DefaultRouter()

router.register('divisoes', DivisaoViewSet)
router.register('nucleos', NucleoViewSet)
router.register('coad', CoadViewSet)
router.register('coad-assessores', CoadAssessorViewSet)
router.register('unidades', UnidadeViewSet)
router.register('editais', EditalViewSet)
router.register('safi-token', SafiToken, basename='Version')

router.registry.extend(contratos_router.registry)
router.registry.extend(usuarios_router.registry)
router.registry.extend(atestes_router.registry)

urlpatterns = [
    path('', include(router.urls))
]
