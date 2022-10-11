from rest_framework import serializers

from ....core.helpers.update_instance_from_dict import update_instance_from_dict
from ...models import Edital, Empresa
from ...models.ata import Ata
from ..utils.historico_utils import serializa_historico_objetos
from ..utils.utils import base64ToFile
from ..validations.contrato_validations import data_encerramento
from .edital_serializer import EditalSimplesSerializer
from .empresa_serializer import EmpresaSerializer
from .produto_ata_serializer import ProdutoAtaSerializer, ProdutoAtaSerializerCreate, ProdutoAtaSigpaeSerializer


class AtaSerializer(serializers.ModelSerializer):
    empresa = EmpresaSerializer()
    edital = EditalSimplesSerializer()
    produtos = ProdutoAtaSerializer(many=True)
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
        return serializa_historico_objetos(obj.historico, obj.numero)

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
            anexo = produto.pop('anexo', '')
            file = base64ToFile(anexo)
            produto['ata'] = ata
            produto_ata = ProdutoAtaSerializerCreate().create(produto)
            produto_ata.anexo.save('anexo.' + file['ext'], file['data'])

        return ata

    def update(self, instance, validated_data):
        produtos = validated_data.pop('produtos', [])
        lista_produtos_existentes = list(instance.produtos.all().values_list('uuid', flat=True))

        for produto in produtos:
            prod = produto.get('uuid', None)
            if prod in lista_produtos_existentes:
                lista_produtos_existentes.remove(prod)
            else:
                anexo = produto.pop('anexo', '')
                file = base64ToFile(anexo)
                produto['ata'] = instance
                produto_ata = ProdutoAtaSerializerCreate().create(produto)
                produto_ata.anexo.save('anexo.' + file['ext'], file['data'])

        # Apaga os produtos que não vieram do payload
        instance.produtos.filter(uuid__in=lista_produtos_existentes).delete()
        update_instance_from_dict(instance, validated_data)
        instance.save()
        return instance

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


class AtaSigpaeSerializer(serializers.ModelSerializer):
    produtos = ProdutoAtaSigpaeSerializer(many=True)

    class Meta:
        model = Ata
        fields = ('numero', 'produtos',)
