from rest_framework import serializers

from ...models import TipoServico


class TipoServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoServico
        fields = ('id', 'nome')
