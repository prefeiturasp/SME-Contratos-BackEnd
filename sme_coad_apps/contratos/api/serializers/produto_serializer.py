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
    durabilidade = serializers.SerializerMethodField()
    armazenabilidade = serializers.SerializerMethodField()
    unidade_medida = serializers.SerializerMethodField()

    def get_unidade_medida(self, obj):
        return {
            'id': obj.unidade_medida,
            'nome': obj.get_unidade_medida_display()
        }

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

    def get_durabilidade(self, obj):
        return {
            'id': obj.durabilidade,
            'nome': obj.get_durabilidade_display()
        }

    def get_armazenabilidade(self, obj):
        return {
            'id': obj.armazenabilidade,
            'nome': obj.get_armazenabilidade_display()
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
    durabilidade = serializers.ChoiceField(required=False, allow_blank=True, choices=Produto.DURABILIDADE_CHOICES)
    armazenabilidade = serializers.ChoiceField(required=True, choices=Produto.ARMAZENABILIDADE_CHOICES)

    def validate(self, attrs):
        categoria = attrs.get('categoria')
        grupo_alimentar = attrs.get('grupo_alimentar')
        durabilidade = attrs.get('durabilidade')
        armazenabilidade = attrs.get('armazenabilidade')
        produto_validation(categoria, grupo_alimentar, durabilidade, armazenabilidade)

        return attrs

    class Meta:
        model = Produto
        exclude = ('id',)


class ProdutoLookUpSerializer(serializers.ModelSerializer):
    categoria = serializers.CharField(source='get_categoria_display')
    grupo_alimentar = serializers.CharField(source='get_grupo_alimentar_display')
    durabilidade = serializers.CharField(source='get_durabilidade_display')
    armazenabilidade = serializers.CharField(source='get_armazenabilidade_display')

    class Meta:
        model = Produto
        fields = ('id', 'uuid', 'nome', 'categoria', 'durabilidade', 'grupo_alimentar', 'armazenabilidade')


class ProdutoSimplesSerializer(serializers.ModelSerializer):
    unidade_medida = serializers.SerializerMethodField()

    def get_unidade_medida(self, obj):
        return obj.unidade_medida.nome if obj.unidade_medida else None

    class Meta:
        model = Produto
        fields = ('id', 'uuid', 'nome', 'unidade_medida')
