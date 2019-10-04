from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..validations.usuario_validations import (senhas_devem_ser_iguais,
                                               registro_funcional_deve_existir,
                                               senha_nao_pode_ser_nulo)
from ....core.api.serializers.divisao_serializer import DivisaoSerializer

user_model = get_user_model()


class UsuarioSerializer(serializers.ModelSerializer):
    divisoes = DivisaoSerializer(many=True)

    def validate_validado(self, username):
        usuario = user_model.objects.filter(username=username)
        if usuario.exists():
            return usuario[0].validado
        else:
            raise serializers.ValidationError({'detail': 'Usuário não encontrado'})

    class Meta:
        model = user_model
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

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('password'))
        instance.validado = True
        instance.save()
        return instance

    class Meta:
        model = user_model
        fields = ['uuid', 'username', 'password', 'password2', 'validado']


class UsuarioLookUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model
        fields = ['nome', 'uuid']
