from django.urls import path, include
from rest_framework import routers

from .api.viewsets.senha_viewset import EsqueciMinhaSenhaViewSet, RedefinirSenhaViewSet
from .api.viewsets.usuario_viewset import UsuarioViewSet

router = routers.DefaultRouter()

router.register('usuarios', UsuarioViewSet, 'Usuários')
router.register('esqueci-minha-senha', EsqueciMinhaSenhaViewSet)
router.register('redefinir-senha', RedefinirSenhaViewSet)

urlpatterns = [
    path('', include(router.urls))
]
