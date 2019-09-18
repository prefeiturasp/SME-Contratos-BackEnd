from django.urls import path, include
from rest_framework import routers

from .api.viewsets.usuario_viewset import UsuarioViewSet

router = routers.DefaultRouter()

router.register('usuarios', UsuarioViewSet, 'Usuários')

#
# from sme_coad_apps.users.views import (
#     user_redirect_view,
#     user_update_view,
#     user_detail_view,
# )
#
# app_name = "users"
urlpatterns = [
    path('', include(router.urls))
    # path("~redirect/", view=user_redirect_view, name="redirect"),
    # path("~update/", view=user_update_view, name="update"),
    # path("<str:username>/", view=user_detail_view, name="detail"),
]
