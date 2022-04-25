from rest_framework import serializers

from ....core.api.serializers.contato_serializer import ContatoSerializer
from ....core.helpers.update_instance_from_dict import update_instance_from_dict
from ...models import Empresa
from ..validations.contrato_validations import tipo_fornecimento


class EmpresaSerializer(serializers.ModelSerializer):
    contatos = ContatoSerializer(many=True)
    cnpj = serializers.SerializerMethodField('get_cnpj')
    tipo_servico = serializers.SerializerMethodField()
    tipo_fornecedor = serializers.SerializerMethodField()
    situacao = serializers.SerializerMethodField()

    def get_cnpj(self, obj):
        return obj.cnpj_formatado

    def get_tipo_servico(self, obj):
        return {
            'id': obj.tipo_servico,
            'nome': obj.get_tipo_servico_display()
        }

    def get_tipo_fornecedor(self, obj):
        return {
            'id': obj.tipo_fornecedor,
            'nome': obj.get_tipo_fornecedor_display()
        }

    def get_situacao(self, obj):
        return {
            'id': obj.situacao,
            'nome': obj.get_situacao_display()
        }

    class Meta:
        model = Empresa
        exclude = ('id',)


class EmpresaCreateSerializer(serializers.ModelSerializer):
    contatos = ContatoSerializer(many=True, required=True)
    nome = serializers.CharField(required=True)
    cnpj = serializers.CharField(required=True)
    razao_social = serializers.CharField(required=True)
    tipo_servico = serializers.ChoiceField(required=True, choices=Empresa.TIPO_SERVICO_CHOICES)
    tipo_fornecedor = serializers.ChoiceField(required=False, allow_blank=True, choices=Empresa.TIPO_FORNECEDOR_CHOICES)
    situacao = serializers.ChoiceField(required=True, choices=Empresa.SITUACAO_CHOICES)
    cep = serializers.CharField(required=True)
    endereco = serializers.CharField(required=True)
    bairro = serializers.CharField(required=True)
    cidade = serializers.CharField(required=True)
    estado = serializers.CharField(required=True)
    numero = serializers.CharField(required=True)
    complemento = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        if attrs.get('tipo_fornecedor'):
            tipo_fornecimento(attrs.get('tipo_servico'))

        return attrs

    def create(self, validated_data):
        contatos = validated_data.pop('contatos', [])
        empresa = Empresa.objects.create(**validated_data)
        for contato in contatos:
            novo_contato = ContatoSerializer().create(validated_data=contato)
            empresa.contatos.add(novo_contato)
        return empresa

    def update(self, instance, validated_data):
        contatos_payload = validated_data.pop('contatos', [])
        instance.contatos.clear()

        lista_contatos = []
        for contato_json in contatos_payload:
            contato = ContatoSerializer().create(contato_json)
            lista_contatos.append(contato)

        update_instance_from_dict(instance, validated_data, save=True)
        instance.contatos.set(lista_contatos)
        return instance

    class Meta:
        model = Empresa
        exclude = ('id',)


class EmpresaLookUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = ('nome', 'uuid', 'id', 'cnpj')
