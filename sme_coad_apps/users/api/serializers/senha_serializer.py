from rest_framework import serializers
from django.contrib.auth import get_user_model

from sme_coad_apps.users.api.validations.usuario_validations import registro_funcional_deve_existir

user_model = get_user_model()


class EsqueciMinhaSenhaSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        registro_funcional_deve_existir(attrs.get('username'))
        return attrs

    class Meta:
        model = user_model
        fields = ['uuid', 'username']


class RedefinirSenhaSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_model
        fields = ['uuid', 'username']
