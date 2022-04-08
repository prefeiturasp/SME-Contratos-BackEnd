from rest_framework import serializers

from ...models import Edital, Empresa
from ...models.ata import Ata
from ..validations.contrato_validations import data_encerramento
from .edital_serializer import EditalListaSerializer
from .empresa_serializer import EmpresaLookUpSerializer


class AtaSerializer(serializers.ModelSerializer):
    empresa = EmpresaLookUpSerializer()
    edital = EditalListaSerializer()
    data_encerramento = serializers.SerializerMethodField()
    data_assinatura = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_data_assinatura(self, obj):
        return obj.data_assinatura.strftime('%d/%m/%Y') if obj.data_assinatura else None

    def get_data_encerramento(self, obj):
        return obj.data_encerramento.strftime('%d/%m/%Y') if obj.data_encerramento else None

    def get_status(self, obj):
        return {
            'id': obj.status,
            'nome': obj.get_status_display()
        }

    class Meta:
        model = Ata
        fields = '__all__'


class AtaCreateSerializer(serializers.ModelSerializer):
    empresa = serializers.SlugRelatedField(
        slug_field='uuid',
        required=False,
        allow_null=True,
        allow_empty=True,
        queryset=Empresa.objects.all()
    )
    edital = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        allow_null=False,
        allow_empty=False,
        queryset=Edital.objects.all()
    )
    numero = serializers.CharField(required=True)
    status = serializers.CharField(required=True)
    unidade_vigencia = serializers.CharField(required=True)
    vigencia = serializers.IntegerField(required=True)
    data_assinatura = serializers.CharField(required=True)
    data_encerramento = serializers.CharField(required=True)

    def validate(self, attrs):
        data_encerramento(attrs.get('unidade_vigencia'), attrs.get('vigencia'),
                          attrs.get('data_assinatura'), attrs.get('data_encerramento'))
        return attrs

    class Meta:
        model = Ata
        exclude = ('id',)
