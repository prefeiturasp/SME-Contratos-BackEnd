from django.urls import path, include
from rest_framework import routers

from .api.viewsets.contrato_viewset import ContratoViewSet

router = routers.DefaultRouter()

router.register('contratos', ContratoViewSet)

urlpatterns = [
    path('', include(router.urls))
]
