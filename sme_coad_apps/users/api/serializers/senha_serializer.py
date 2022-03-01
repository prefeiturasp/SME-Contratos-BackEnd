import environ
from django.contrib.auth import get_user_model
from rest_framework import serializers

from ...tasks import enviar_email_redefinicao_senha
from ..validations.usuario_validations import (
    hash_redefinicao_deve_existir,
    registro_funcional_deve_existir,
    senha_nao_pode_ser_nulo,
    senhas_devem_ser_iguais,
    usuario_deve_estar_ativo,
    usuario_precisa_estar_validado
)

user_model = get_user_model()
env = environ.Env()


class EsqueciMinhaSenhaSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    def validate(self, attrs):
        registro_funcional_deve_existir(attrs.get('username'))
        usuario_precisa_estar_validado(attrs.get('username'))
        usuario_deve_estar_ativo(attrs.get('username'))
        return attrs

    def update(self, instance, validated_data):
        instance.hash_redefinicao = instance.encode_hash
        instance.save()

        enviar_email_redefinicao_senha.delay(email=instance.email, username=instance.username, nome=instance.nome,
                                             hash_redefinicao=instance.hash_redefinicao)
        return instance

    class Meta:
        model = user_model
        fields = ['username', 'email']


class RedefinirSenhaSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        hash_redefinicao = attrs.get('hash_redefinicao')
        hash_redefinicao_deve_existir(hash_redefinicao)
        return attrs

    class Meta:
        model = user_model
        fields = ['uuid', 'username']


class RedefinirSenhaSerializerCreator(serializers.ModelSerializer):
    password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        hash_redefinicao = attrs.get('hash_redefinicao')
        hash_redefinicao_deve_existir(hash_redefinicao)
        senha_nao_pode_ser_nulo(attrs.get('password'))
        senha_nao_pode_ser_nulo(attrs.get('password2'))
        senhas_devem_ser_iguais(attrs.get('password'), attrs.get('password2'))
        attrs.pop('password2')
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('password'))
        instance.is_active = True
        instance.hash_redefinicao = ''
        instance.save()
        return instance

    class Meta:
        model = user_model
        fields = ['hash_redefinicao', 'password', 'password2']
