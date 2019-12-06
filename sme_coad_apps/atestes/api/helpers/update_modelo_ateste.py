from sme_coad_apps.atestes.api.serializers.grupo_verificacao_serializer import GrupoVerificacaoSerializerCreate
from sme_coad_apps.atestes.api.serializers.intens_verificacao_serializer import ItensVerificacaoSerializeCreate


def salvar_grupo(modelo, grupo_verificacao):
    itens_verificacao = grupo_verificacao.pop('itens_de_verificacao')
    grupo_verificacao['modelo'] = modelo
    grupo = GrupoVerificacaoSerializerCreate().create(grupo_verificacao)
    for item in itens_verificacao:
        item['grupo'] = grupo
        ItensVerificacaoSerializeCreate().create(item)
    return grupo
