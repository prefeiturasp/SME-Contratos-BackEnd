from datetime import timedelta

from rest_framework import fields, serializers

from ...models.contrato import Contrato
from ...models.intercorrencia import Rescisao, Suspensao
from ..validations.contrato_validations import validacao_data_rescisao


class RescisaoSerializer(serializers.ModelSerializer):
    contrato = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        allow_null=False,
        allow_empty=False,
        queryset=Contrato.objects.all()
    )

    class Meta:
        model = Rescisao
        exclude = ('id',)


class RescisaoCreateSerializer(serializers.ModelSerializer):
    contrato = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        allow_null=False,
        allow_empty=False,
        queryset=Contrato.objects.all()
    )
    data_encerramento = serializers.DateField(required=False)
    motivo_rescisao = fields.MultipleChoiceField(choices=Rescisao.MOTIVO_RESCICAO_CHOICES)

    def validate(self, attrs):
        if attrs['tipo_intercorrencia'] == 'RESCISAO':
            validacao_data_rescisao(attrs)
        return attrs

    def create(self, validated_data):
        validated_data['data_encerramento'] = validated_data.get('data_rescisao')
        intercorrencia = Rescisao.objects.create(**validated_data)

        return intercorrencia

    class Meta:
        model = Rescisao
        exclude = ('id',)


class SuspensaoSerializer(serializers.ModelSerializer):
    contrato = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        allow_null=False,
        allow_empty=False,
        queryset=Contrato.objects.all()
    )

    class Meta:
        model = Suspensao
        exclude = ('id',)


class SuspensaoCreateSerializer(serializers.ModelSerializer):
    contrato = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        allow_null=False,
        allow_empty=False,
        queryset=Contrato.objects.all()
    )
    data_encerramento = serializers.DateField(required=False)

    def create(self, validated_data):
        acrescentar_dias = validated_data.get('acrescentar_dias', False)
        data_inicial = validated_data.get('data_inicial', None)
        data_final = validated_data.get('data_final', None)
        data_encerramento_contrato = validated_data.get('contrato').data_encerramento
        dias = (data_final - data_inicial).days
        if data_encerramento_contrato:
            validated_data['data_encerramento'] = (data_encerramento_contrato + timedelta(dias + 1) if acrescentar_dias
                                                   else data_encerramento_contrato)
        intercorrencia = Suspensao.objects.create(**validated_data)

        return intercorrencia

    class Meta:
        model = Suspensao
        exclude = ('id',)
