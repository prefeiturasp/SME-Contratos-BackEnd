from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from ...models import Produto, UnidadeDeMedida
from ..validations.contrato_validations import produto_validation


class UnidadeDeMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadeDeMedida
        fields = ('nome', 'uuid', 'id')


class ProdutoSerializer(serializers.ModelSerializer):
    categoria = serializers.SerializerMethodField()
    situacao = serializers.SerializerMethodField()
    grupo_alimentar = serializers.SerializerMethodField()
    tipo_programa = serializers.SerializerMethodField()
    unidade_medida = UnidadeDeMedidaSerializer()

    def get_categoria(self, obj):
        return {
            'id': obj.categoria,
            'nome': obj.get_categoria_display()
        }

    def get_situacao(self, obj):
        return {
            'id': obj.situacao,
            'nome': obj.get_situacao_display()
        }

    def get_grupo_alimentar(self, obj):
        return {
            'id': obj.grupo_alimentar,
            'nome': obj.get_grupo_alimentar_display()
        }

    def get_tipo_programa(self, obj):
        return {
            'id': obj.tipo_programa,
            'nome': obj.get_tipo_programa_display()
        }

    class Meta:
        model = Produto
        exclude = ('id',)


class ProdutoCreateSerializer(serializers.ModelSerializer):
    unidade_medida = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        queryset=UnidadeDeMedida.objects.all()
    )
    nome = serializers.CharField(required=True,
                                 validators=[UniqueValidator(queryset=Produto.objects.all(),
                                                             message='Já existe um produto com este nome cadastrado!')])
    categoria = serializers.ChoiceField(required=True, choices=Produto.CATEGORIA_CHOICES)
    situacao = serializers.ChoiceField(required=True, choices=Produto.SITUACAO_CHOICES)
    grupo_alimentar = serializers.ChoiceField(required=False, allow_blank=True, choices=Produto.GRUPO_ALIMENTAR_CHOICES)
    tipo_programa = serializers.ChoiceField(required=False, allow_blank=True, choices=Produto.TIPO_PROGRAMA_CHOICES)

    def validate(self, attrs):
        categoria = attrs.get('categoria')
        grupo_alimentar = attrs.get('grupo_alimentar')
        tipo_programa = attrs.get('tipo_programa')
        produto_validation(categoria, grupo_alimentar, tipo_programa)

        return attrs

    class Meta:
        model = Produto
        exclude = ('id',)


class ProdutoLookUpSerializer(serializers.ModelSerializer):
    categoria = serializers.CharField(source='get_categoria_display')
    grupo_alimentar = serializers.CharField(source='get_grupo_alimentar_display')
    tipo_programa = serializers.CharField(source='get_tipo_programa_display')

    class Meta:
        model = Produto
        fields = ('id', 'uuid', 'nome', 'categoria', 'grupo_alimentar', 'tipo_programa')


class ProdutoSimplesSerializer(serializers.ModelSerializer):
    unidade_medida = serializers.SerializerMethodField()

    def get_unidade_medida(self, obj):
        return obj.unidade_medida.nome if obj.unidade_medida else None

    class Meta:
        model = Produto
        fields = ('uuid', 'nome', 'unidade_medida')
