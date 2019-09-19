from django.urls import path, include
from rest_framework import routers

from .api.viewsets.divisao_viewset import DivisaoViewSet
from .api.viewsets.nucleo_viewsets import NucleoViewSet

router = routers.DefaultRouter()

router.register('divisao', DivisaoViewSet)
router.register('nucleo', NucleoViewSet)

urlpatterns = [
    path('', include(router.urls))
]
