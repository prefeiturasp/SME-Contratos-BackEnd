from django.urls import path, include
from rest_framework import routers

from .api.viewsets.modelo_ateste_viewset import ModeloAtesteViewSet

router = routers.DefaultRouter()

router.register('modelo-ateste', ModeloAtesteViewSet)

urlpatterns = [
    path('', include(router.urls))
]
