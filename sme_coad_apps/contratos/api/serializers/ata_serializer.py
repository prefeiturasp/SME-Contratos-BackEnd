from rest_framework import serializers

from ...models import Edital, Empresa
from ...models.ata import Ata
from ..utils.historico_utils import serializa_historico
from ..validations.contrato_validations import data_encerramento
from .edital_serializer import EditalSimplesSerializer
from .empresa_serializer import EmpresaSerializer
from .produto_ata_serializer import ProdutoAtaSerializer, ProdutoAtaSerializerCreate


class AtaSerializer(serializers.ModelSerializer):
    empresa = EmpresaSerializer()
    edital = EditalSimplesSerializer()
    produtos = serializers.SerializerMethodField()
    data_encerramento = serializers.SerializerMethodField()
    data_assinatura = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    historico = serializers.SerializerMethodField()

    def get_data_assinatura(self, obj):
        return obj.data_assinatura.strftime('%d/%m/%Y') if obj.data_assinatura else None

    def get_data_encerramento(self, obj):
        return obj.data_encerramento.strftime('%d/%m/%Y') if obj.data_encerramento else None

    def get_status(self, obj):
        return {
            'id': obj.status,
            'nome': obj.get_status_display()
        }

    def get_historico(self, obj):
        return serializa_historico(obj.historico)

    def get_produtos(self, obj):
        produto = obj.produtos.all().order_by('id')
        return ProdutoAtaSerializer(produto, many=True).data

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
    produtos = ProdutoAtaSerializerCreate(many=True, required=False)

    def validate(self, attrs):
        data_encerramento(attrs.get('unidade_vigencia'), attrs.get('vigencia'),
                          attrs.get('data_assinatura'), attrs.get('data_encerramento'))
        return attrs

    def create(self, validated_data):
        produtos = validated_data.pop('produtos', [])
        ata = Ata.objects.create(**validated_data)

        for produto in produtos:
            produto['ata'] = ata
            ProdutoAtaSerializerCreate().create(produto)

        return ata

    class Meta:
        model = Ata
        exclude = ('id',)


class AtaLookUpSerializer(serializers.ModelSerializer):
    nome_empresa = serializers.SerializerMethodField()
    objeto = serializers.SerializerMethodField()
    data_encerramento = serializers.SerializerMethodField()
    status = serializers.CharField(source='get_status_display')

    def get_nome_empresa(self, obj):
        return obj.empresa.nome if obj.empresa else None

    def get_objeto(self, obj):
        return obj.edital.objeto.nome if obj.edital and obj.edital.objeto else None

    def get_data_encerramento(self, obj):
        return obj.data_encerramento.strftime('%d/%m/%Y') if obj.data_encerramento else None

    class Meta:
        model = Ata
        fields = ('uuid', 'numero', 'nome_empresa', 'status', 'data_encerramento', 'objeto')
