from rest_framework import serializers

from sme_coad_apps.core.api.serializers.divisao_serializer import DivisaoSerializer
from ...models import User


class UsuarioSerializer(serializers.ModelSerializer):
    divisoes = DivisaoSerializer(many=True)

    class Meta:
        model = User
        fields = ['uuid', 'username', 'nome', 'divisoes']
