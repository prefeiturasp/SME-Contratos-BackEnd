from rest_framework import serializers

from sme_coad_apps.core.api.serializers.divisao_serializer import DivisaoSerializer
from sme_coad_apps.users.api.validations.usuario_validations import senhas_devem_ser_iguais, \
    registro_funcional_deve_existir
from ...models import User


class UsuarioSerializer(serializers.ModelSerializer):
    divisoes = DivisaoSerializer(many=True)

    class Meta:
        model = User
        fields = ['uuid', 'username', 'nome', 'divisoes', 'validado']


class UsuarioSerializerCreators(serializers.ModelSerializer):
    password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        senhas_devem_ser_iguais(attrs.get('password'), attrs.get('password2'))
        registro_funcional_deve_existir(attrs.get('username'))
        attrs.pop('password2')
        return attrs

    class Meta:
        model = User
        fields = ['uuid', 'username', 'password', 'password2', 'validado']
