from rest_framework import serializers

from ...models import Nucleo


class NucleoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nucleo
        fields = '__all__'


class NucleoSerializerCreator(serializers.ModelSerializer):
    class Meta:
        model = Nucleo
        fields = '__all__'
