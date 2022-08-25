from datetime import timedelta

from rest_framework import serializers

from ...models.contrato import Contrato
from ...models.intercorrencia import Intercorrencia


class IntercorrenciaSerializer(serializers.ModelSerializer):
    contrato = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        allow_null=False,
        allow_empty=False,
        queryset=Contrato.objects.all()
    )

    class Meta:
        model = Intercorrencia
        exclude = ('id',)


class IntercorrenciaCreateSerializer(serializers.ModelSerializer):
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
        data_encerramento_contrato = Contrato.objects.get(uuid=validated_data.get('contrato').uuid).data_encerramento
        dias = (data_final - data_inicial).days
        if data_encerramento_contrato:
            validated_data['data_encerramento'] = (data_encerramento_contrato + timedelta(dias + 1) if acrescentar_dias
                                                   else data_encerramento_contrato)
        intercorrencia = Intercorrencia.objects.create(**validated_data)

        return intercorrencia

    class Meta:
        model = Intercorrencia
        exclude = ('id',)
