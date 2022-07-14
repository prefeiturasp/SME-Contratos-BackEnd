import environ
from rest_framework import serializers

from ...models.contrato import AnexoContrato, Contrato

env = environ.Env()
API_URL = f'{env("API_URL")}'


class AnexoContratolSerializer(serializers.ModelSerializer):

    contrato = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        queryset=Contrato.objects.all()
    )
    anexo = serializers.SerializerMethodField('get_anexo')

    def get_anexo(self, obj):
        if bool(obj.anexo):
            return '%s%s' % (API_URL, obj.anexo.url)
        else:
            return None

    class Meta:
        model = AnexoContrato
        exclude = ('id',)


class AnexoContratoCreateSerializer(serializers.ModelSerializer):

    contrato = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        queryset=Contrato.objects.all()
    )

    class Meta:
        model = AnexoContrato
        exclude = ('id',)
