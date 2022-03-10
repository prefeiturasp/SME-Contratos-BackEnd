from django_filters import rest_framework as filters


class ContratoFilter(filters.FilterSet):
    uuid = filters.CharFilter(
        field_name='uuid',
        lookup_expr='exact',
    )
    termo_contrato = filters.CharFilter(
        field_name='termo_contrato',
        lookup_expr='icontains',
    )
    status = filters.CharFilter(
        field_name='situacao',
        lookup_expr='exact',
    )
    cnpj_empresa = filters.CharFilter(
        field_name='empresa_contratada__cnpj',
        lookup_expr='exact',
    )
    nome_empresa = filters.CharFilter(
        field_name='empresa_contratada__nome',
        lookup_expr='icontains',
    )
    empresa = filters.CharFilter(
        field_name='empresa_contratada__uuid',
        lookup_expr='exact',
    )
    objeto = filters.CharFilter(
        field_name='tipo_servico__id',
        lookup_expr='exact',
    )
    data_inicial = filters.DateFilter(
        field_name='data_encerramento',
        lookup_expr='gte',
    )
    data_final = filters.DateFilter(
        field_name='data_encerramento',
        lookup_expr='lte',
    )


class EditalFilter(filters.FilterSet):
    uuid = filters.CharFilter(
        field_name='uuid',
        lookup_expr='exact',
    )
    numero = filters.CharFilter(
        field_name='numero',
        lookup_expr='exact',
    )
    status = filters.CharFilter(
        field_name='status',
        lookup_expr='exact',
    )
    tipo_contratacao = filters.CharFilter(
        field_name='tipo_contratacao',
        lookup_expr='exact',
    )
    objeto = filters.CharFilter(
        field_name='tipo_servico__id',
        lookup_expr='exact',
    )
    data_inicial = filters.DateFilter(
        field_name='data_homologacao',
        lookup_expr='gte',
    )
    data_final = filters.DateFilter(
        field_name='data_homologacao',
        lookup_expr='lte',
    )
