from rest_framework import fields, serializers

from ...models.aditamento import Aditamento
from ...models.contrato import Contrato
from ..validations.contrato_validations import validacao_objetos_aditamento


class AditamentoSerializer(serializers.ModelSerializer):
    contrato = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        allow_null=False,
        allow_empty=False,
        queryset=Contrato.objects.all()
    )
    objeto_aditamento = serializers.SerializerMethodField()

    def get_objeto_aditamento(self, obj):
        result = []
        for objeto in obj.objeto_aditamento:
            result.append(obj.OBJETOS_NOMES[objeto])
        return result

    class Meta:
        model = Aditamento
        exclude = ('id',)


class AditamentoLookUpSerializer(serializers.ModelSerializer):
    contrato = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        allow_null=False,
        allow_empty=False,
        queryset=Contrato.objects.all()
    )
    objeto_aditamento = serializers.SerializerMethodField()

    def get_objeto_aditamento(self, obj):
        result = []
        for objeto in obj.objeto_aditamento:
            result.append(obj.OBJETOS_NOMES[objeto])
        return result

    class Meta:
        model = Aditamento
        exclude = ('id', 'criado_em', 'alterado_em')


class AditamentoCreateSerializer(serializers.ModelSerializer):
    contrato = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        allow_null=False,
        allow_empty=False,
        queryset=Contrato.objects.all()
    )
    objeto_aditamento = fields.MultipleChoiceField(choices=Aditamento.OBJETO_CHOICES)

    @classmethod
    def get_serializer(cls, model):
        if model == Aditamento:
            return AditamentoSerializer

    def to_representation(self, instance):
        serializer = self.get_serializer(instance.__class__)
        return serializer(instance, context=self.context).data

    def validate(self, attrs):
        validacao_objetos_aditamento(attrs)
        return attrs

    class Meta:
        model = Aditamento
        exclude = ('id',)
