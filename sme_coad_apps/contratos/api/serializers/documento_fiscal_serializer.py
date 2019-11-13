from rest_framework import serializers

from ...models.contrato import DocumentoFiscal, Contrato


class DocumentoFiscalSerializer(serializers.ModelSerializer):
    contrato = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        queryset=Contrato.objects.all()
    )

    class Meta:
        model = DocumentoFiscal
        exclude = ('id',)
