from rest_framework import serializers

from sme_coad_apps.core.api.serializers.divisao_serializer import DivisaoSerializer
from sme_coad_apps.users.api.validations.usuario_validations import senhas_devem_ser_iguais, \
    registro_funcional_deve_existir, senha_nao_pode_ser_nulo
from ...models import User


class UsuarioSerializer(serializers.ModelSerializer):
    divisoes = DivisaoSerializer(many=True)

    class Meta:
        model = User
        fields = ['uuid', 'username', 'nome', 'divisoes', 'validado']


class UsuarioSerializerCreators(serializers.ModelSerializer):
    password2 = serializers.CharField(required=False)

    def validate(self, attrs):
        senhas_devem_ser_iguais(attrs.get('password'), attrs.get('password2'))
        registro_funcional_deve_existir(attrs.get('username'))
        senha_nao_pode_ser_nulo(attrs.get('password'), 'Senha')
        senha_nao_pode_ser_nulo(attrs.get('password2'), 'Senha 2')
        attrs.pop('password2')
        return attrs

    class Meta:
        model = User
        fields = ['uuid', 'username', 'password', 'password2', 'validado']
