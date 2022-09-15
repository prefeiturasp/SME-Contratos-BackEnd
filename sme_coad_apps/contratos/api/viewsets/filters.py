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
        field_name='objeto__id',
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
    cnpj_empresa = filters.CharFilter(
        field_name='empresa__cnpj',
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
        field_name='objeto__id',
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


class AtaFilter(filters.FilterSet):
    uuid = filters.CharFilter(
        field_name='uuid',
        lookup_expr='exact',
    )
    numero = filters.CharFilter(
        field_name='numero',
        lookup_expr='icontains',
    )
    cnpj_empresa = filters.CharFilter(
        field_name='empresa__cnpj',
        lookup_expr='exact',
    )
    empresa = filters.CharFilter(
        field_name='empresa__uuid',
        lookup_expr='exact',
    )
    status = filters.CharFilter(
        field_name='status',
        lookup_expr='exact',
    )
    objeto = filters.CharFilter(
        field_name='edital__objeto__id',
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


class EmpresaFilter(filters.FilterSet):
    uuid = filters.CharFilter(
        field_name='uuid',
        lookup_expr='exact',
    )
    nome = filters.CharFilter(
        field_name='nome',
        lookup_expr='icontains',
    )
    cnpj_empresa = filters.CharFilter(
        field_name='cnpj',
        lookup_expr='exact',
    )
    tipo_servico = filters.CharFilter(
        field_name='tipo_servico',
        lookup_expr='exact',
    )
    tipo_fornecedor = filters.CharFilter(
        field_name='tipo_fornecedor',
        lookup_expr='exact',
    )
    situacao = filters.CharFilter(
        field_name='situacao',
        lookup_expr='exact',
    )


class ProdutoFilter(filters.FilterSet):
    uuid = filters.CharFilter(
        field_name='uuid',
        lookup_expr='exact',
    )
    nome = filters.CharFilter(
        field_name='nome',
        lookup_expr='icontains',
    )
    situacao = filters.CharFilter(
        field_name='situacao',
        lookup_expr='exact',
    )
    categoria = filters.CharFilter(
        field_name='categoria',
        lookup_expr='exact',
    )
    grupo_alimentar = filters.CharFilter(
        field_name='grupo_alimentar',
        lookup_expr='exact',
    )
    tipo_programa = filters.CharFilter(
        field_name='tipo_programa',
        lookup_expr='exact',
    )
