from django.urls import path, include
from rest_framework import routers

from .api.viewsets.usuario_viewset import UsuarioViewSet

router = routers.DefaultRouter()
router.register('usuario', UsuarioViewSet)

urlpatterns = [
    path('', include(router.urls))
]
