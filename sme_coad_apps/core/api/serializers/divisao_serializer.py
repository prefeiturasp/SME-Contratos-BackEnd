from rest_framework import serializers

from ...models import Divisao


class DivisaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Divisao
        fields = '__all__'


class DivisaoSerializerCreator(serializers.ModelSerializer):
    class Meta:
        model = Divisao
        fields = '__all__'


class DivisaoLookUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Divisao
        fields = ('sigla', 'uuid')
