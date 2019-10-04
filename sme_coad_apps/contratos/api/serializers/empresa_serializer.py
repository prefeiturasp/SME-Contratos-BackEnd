from rest_framework import serializers

from ...models import Empresa


class EmpresaLookUpSerializer(serializers.ModelSerializer):
    cnpj = serializers.SerializerMethodField('get_cnpj')

    def get_cnpj(self, obj):
        return obj.cnpj_formatado

    class Meta:
        model = Empresa
        fields = ('nome', 'cnpj', 'uuid')
