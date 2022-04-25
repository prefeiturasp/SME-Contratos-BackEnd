from rest_framework import serializers

from ...models.contato import Contato


class ContatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contato
        exclude = ('id',)
