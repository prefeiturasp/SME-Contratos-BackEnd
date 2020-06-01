from ..serializers.grupo_obrigacao_serializer import GrupoObrigacaoSerializerCreate
from ..serializers.obrigacao_serializer import ObrigacaoSerializeCreate


def salvar_itens_de_grupo(edital, grupo_obrigacao):
    itens_obrigacao = grupo_obrigacao.pop('itens_de_obrigacao')
    grupo_obrigacao['edital'] = edital
    grupo = GrupoObrigacaoSerializerCreate().create(grupo_obrigacao)
    for item in itens_obrigacao:
        item['grupo'] = grupo
        ObrigacaoSerializeCreate().create(item)
    return grupo
