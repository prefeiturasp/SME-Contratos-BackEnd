from django.urls import include, path
from rest_framework import routers

from .api import viewsets

router = routers.DefaultRouter()
router.register('equipamentos', viewsets.EquipamentosEOLViewSet, basename='Equipamentos')

urlpatterns = [
    path('', include(router.urls)),
]
