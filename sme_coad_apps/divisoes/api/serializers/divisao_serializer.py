from rest_framework import serializers

from sme_coad_apps.divisoes.models import Divisao


class DivisaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Divisao
        exclude = ('id', 'descricao')


class DivisaoSerializerCreator(serializers.ModelSerializer):
    class Meta:
        model = Divisao
        fields = '__all__'
