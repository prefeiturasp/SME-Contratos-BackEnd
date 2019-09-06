from rest_framework import serializers

from sme_coad_apps.divisoes.models import Nucleo


class NucleoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nucleo
        exclude = ('id',)


class NucleoSerializerCreator(serializers.ModelSerializer):
    class Meta:
        model = Nucleo
        exclude = ('id',)
