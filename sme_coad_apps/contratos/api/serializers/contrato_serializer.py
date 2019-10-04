from rest_framework import serializers

from ...api.serializers.empresa_serializer import EmpresaLookUpSerializer
from ...api.serializers.tipo_servico_serializer import TipoServicoSerializer
from ...models import Contrato
from ....core.api.serializers.nucleo_serializer import NucleoLookUpSerializer
from ....users.api.serializers.usuario_serializer import UsuarioLookUpSerializer


class ContratoSerializer(serializers.ModelSerializer):
    data_encerramento = serializers.SerializerMethodField('get_data_encerramento')
    tipo_servico = TipoServicoSerializer()
    empresa_contratada = EmpresaLookUpSerializer()
    nucleo_responsavel = NucleoLookUpSerializer()
    gestor = UsuarioLookUpSerializer()

    def get_data_encerramento(self, obj):
        return obj.data_encerramento

    class Meta:
        model = Contrato
        fields = '__all__'
