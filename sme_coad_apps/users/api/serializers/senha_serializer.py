import environ
from django.contrib.auth import get_user_model
from rest_framework import serializers

from sme_coad_apps.core.helpers.enviar_email import enviar_email
from ..validations.usuario_validations import (registro_funcional_deve_existir,
                                               usuario_precisa_estar_validado,
                                               hash_redefinicao_deve_existir, senha_nao_pode_ser_nulo,
                                               senhas_devem_ser_iguais)

user_model = get_user_model()
env = environ.Env()


class EsqueciMinhaSenhaSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        registro_funcional_deve_existir(attrs.get('username'))
        usuario_precisa_estar_validado(attrs.get('username'))
        return attrs

    def update(self, instance, validated_data):
        try:
            instance.is_active = False
            instance.hash_redefinicao = instance.encode_hash
            instance.save()
            link = 'http://{}/redefinir-senha/?hash={}'.format(env('SERVER_NAME'), instance.hash_redefinicao)
            enviar_email(
                'Solicitação de redefinição de senha',
                'Link: <a href="{}">Clique aqui</a>'.format(link),
                instance.email
            )
            return instance
        except serializers.ValidationError(detail='Ocorreu um error ao tentar lembrar da senha'):
            pass

    class Meta:
        model = user_model
        fields = ['uuid', 'username']


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
