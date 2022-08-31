from datetime import date, timedelta

import environ
from rest_framework import fields, serializers

from ...models.contrato import Contrato
from ...models.intercorrencia import AnexoImpedimento, Impedimento, Rescisao, Suspensao
from ..validations.contrato_validations import validacao_data_inicial_final, validacao_data_rescisao

env = environ.Env()
API_URL = f'{env("API_URL")}'


class AnexoImpedimentoSerializer(serializers.ModelSerializer):

    impedimento = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        queryset=Impedimento.objects.all()
    )
    anexo = serializers.SerializerMethodField('get_anexo')

    def get_anexo(self, obj):
        if bool(obj.anexo):
            return '%s%s' % (API_URL, obj.anexo.url)
        else:
            return None

    class Meta:
        model = AnexoImpedimento
        exclude = ('id',)


class AnexoImpedimentoLookUpSerializer(serializers.ModelSerializer):
    anexo = serializers.SerializerMethodField('get_anexo')

    def get_anexo(self, obj):
        if bool(obj.anexo):
            return '%s%s' % (API_URL, obj.anexo.url)
        else:
            return None

    class Meta:
        model = AnexoImpedimento
        fields = ('anexo',)


class AnexoImpedimentoCreateSerializer(serializers.ModelSerializer):

    impedimento = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        queryset=Impedimento.objects.all()
    )

    class Meta:
        model = AnexoImpedimento
        exclude = ('id',)


class ImpedimentoSerializer(serializers.ModelSerializer):
    contrato = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        allow_null=False,
        allow_empty=False,
        queryset=Contrato.objects.all()
    )
    tipo_intercorrencia = serializers.CharField(source='get_tipo_intercorrencia_display')
    dias_impedimento = serializers.SerializerMethodField('get_dias_impedimento')
    vigencia = serializers.SerializerMethodField('get_dias_vigencia')
    anexos_impedimento = serializers.SerializerMethodField('get_anexos_impedimento')

    def get_anexos_impedimento(self, obj):
        anexos = obj.anexos_impedimento.all()
        anexos_set = AnexoImpedimentoLookUpSerializer(anexos, many=True)
        return anexos_set.data

    def get_dias_impedimento(self, obj):
        dias_impedimento = (obj.data_final - obj.data_inicial).days + 1
        return f'{dias_impedimento} dias'

    def get_dias_vigencia(self, obj):
        hoje = date.today()
        dias_impedimentos = (obj.data_final - obj.data_inicial).days + 1
        contrato = obj.contrato
        data_inicio_contrato = (contrato.data_assinatura if contrato.referencia_encerramento == 'DATA_ASSINATURA'
                                else contrato.data_ordem_inicio)
        if data_inicio_contrato <= hoje <= obj.data_encerramento:
            if obj.data_inicial <= hoje <= obj.data_final:
                vigencia = contrato.vigencia - (obj.data_inicial - data_inicio_contrato).days
            elif hoje > obj.data_final:
                vigencia = contrato.vigencia - (hoje - data_inicio_contrato).days - 1 + dias_impedimentos
            else:
                vigencia = contrato.vigencia - (hoje - data_inicio_contrato).days - 1
        elif hoje < data_inicio_contrato:
            vigencia = obj.vigencia
        else:
            vigencia = 0
        return vigencia

    class Meta:
        model = Impedimento
        exclude = ('id',)


class ImpedimentoCreateSerializer(serializers.ModelSerializer):
    contrato = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        allow_null=False,
        allow_empty=False,
        queryset=Contrato.objects.all()
    )
    data_encerramento = serializers.DateField(required=False)

    def validate(self, attrs):
        if attrs['tipo_intercorrencia'] == 'IMPEDIMENTO':
            validacao_data_inicial_final(attrs)
        return attrs

    def create(self, validated_data):
        data_inicial = validated_data.get('data_inicial', None)
        data_final = validated_data.get('data_final', None)
        contrato = validated_data.get('contrato')
        data_inicio_contrato = (contrato.data_assinatura if contrato.referencia_encerramento == 'DATA_ASSINATURA'
                                else contrato.data_ordem_inicio)
        vigencia_contrato = contrato.vigencia
        data_encerramento_contrato = data_inicio_contrato + timedelta(vigencia_contrato)
        dias_impedimento = (data_final - data_inicial).days
        validated_data['data_encerramento'] = data_encerramento_contrato + timedelta(dias_impedimento)
        validated_data['vigencia'] = vigencia_contrato
        intercorrencia = Impedimento.objects.create(**validated_data)

        return intercorrencia

    class Meta:
        model = Impedimento
        exclude = ('id',)


class RescisaoSerializer(serializers.ModelSerializer):
    contrato = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        allow_null=False,
        allow_empty=False,
        queryset=Contrato.objects.all()
    )
    tipo_intercorrencia = serializers.CharField(source='get_tipo_intercorrencia_display')
    motivo_rescisao = serializers.SerializerMethodField('get_motivo_rescisao')

    def get_motivo_rescisao(self, obj):
        lista = []
        for i in obj.motivo_rescisao:
            lista.append(obj.MOTIVO_RESCISAO_NOMES[i])
        return lista

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
    tipo_intercorrencia = serializers.CharField(source='get_tipo_intercorrencia_display')
    motivo_suspensao = serializers.CharField(source='get_motivo_suspensao_display')
    dias_suspensao = serializers.SerializerMethodField('get_dias_suspensao')

    def get_dias_suspensao(self, obj):
        dias_suspensao = (obj.data_final - obj.data_inicial).days + 1
        return f'{dias_suspensao} dias'

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
