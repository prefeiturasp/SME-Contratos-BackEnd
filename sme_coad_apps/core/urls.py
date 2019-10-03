from django.urls import path, include
from rest_framework import routers

from sme_coad_apps.contratos.urls import router as contratos_router
from sme_coad_apps.users.urls import router as usuarios_router
from .api.viewsets.divisao_viewset import DivisaoViewSet
from .api.viewsets.nucleo_viewsets import NucleoViewSet

router = routers.DefaultRouter()

router.register('divisoes', DivisaoViewSet)
router.register('nucleos', NucleoViewSet)

router.registry.extend(contratos_router.registry)
router.registry.extend(usuarios_router.registry)

urlpatterns = [
    path('', include(router.urls))
]
