from ...api.serializers.grupo_obrigacao_serializer import GrupoObrigacaoSerializerCreate
from ...api.serializers.obrigacao_serializer import ObrigacaoSerializeCreate


def salvar_itens_de_grupo(edital, grupo_obrigacao):
    itens_obrigacao = grupo_obrigacao.pop('itens_de_obrigacao')
    grupo_obrigacao['edital'] = edital
    grupo = GrupoObrigacaoSerializerCreate().create(grupo_obrigacao)
    for item in itens_obrigacao:
        item['grupo'] = grupo
        ObrigacaoSerializeCreate().create(item)
    return grupo


def log_create(edital, user=None):
    import json
    from datetime import datetime

    historico = {'created_at': datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
                 'user': {'uuid': str(user.uuid), 'email': user.email} if user else user,
                 'action': 'CREATE'}

    lista_grupos = []
    for grupo in edital.grupos_de_obrigacao.all():
        itens_obrigacao = [
            {'uuid': str(obrigacao.uuid), 'item': obrigacao.item, 'descricao': obrigacao.descricao}
            for obrigacao in grupo.itens_de_obrigacao.all()]

        lista_grupos.append({
            'uuid': {'from': None, 'to': str(grupo.uuid)},
            'nome': {'from': None, 'to': grupo.nome},
            'itens_obrigacao': {'from': None, 'to': itens_obrigacao}
        })

    historico['changes'] = [
        {'field': 'criado_em', 'from': None, 'to': edital.criado_em.strftime('%Y-%m-%d %H:%M:%S')},
        {'field': 'numero', 'from': None, 'to': edital.numero},
        {'field': 'processo', 'from': None, 'to': edital.processo},
        {'field': 'tipo_contratacao', 'from': None, 'to': edital.tipo_contratacao},
        {'field': 'subtipo', 'from': None, 'to': edital.subtipo},
        {'field': 'status', 'from': None, 'to': edital.status},
        {'field': 'data_homologacao', 'from': None, 'to': edital.data_homologacao.strftime('%Y-%m-%d')},
        {'field': 'uuid', 'from': None, 'to': str(edital.uuid)},
        {'field': 'objeto', 'from': None, 'to': edital.objeto.nome},
        {'field': 'descricao_objeto', 'from': None, 'to': edital.descricao_objeto},
        {'field': 'grupos_obrigacoes', 'changes': lista_grupos},
    ]

    edital.historico = json.dumps([historico])
    edital.save()


def diff_edital(instance, validated_data):
    changes = []
    if instance.numero != validated_data['numero']:
        changes.append(
            {'field': 'numero', 'from': instance.numero, 'to': validated_data['numero']})

    if instance.processo != validated_data['processo']:
        changes.append(
            {'field': 'processo', 'from': instance.processo, 'to': validated_data['processo']})

    if instance.tipo_contratacao != validated_data['tipo_contratacao']:
        changes.append(
            {'field': 'tipo_contratacao', 'from': instance.tipo_contratacao, 'to': validated_data['tipo_contratacao']})

    if instance.subtipo != validated_data['subtipo']:
        changes.append(
            {'field': 'subtipo', 'from': instance.subtipo, 'to': validated_data['subtipo']})

    if instance.status != validated_data['status']:
        changes.append(
            {'field': 'status', 'from': instance.status, 'to': validated_data['status']})

    if instance.data_homologacao.strftime('%Y-%m-%d') != validated_data['data_homologacao'].strftime('%Y-%m-%d'):
        changes.append(
            {
                'field': 'data_homologacao',
                'from': instance.data_homologacao.strftime('%Y-%m-%d'),
                'to': validated_data['data_homologacao'].strftime('%Y-%m-%d')
            }
        )

    if instance.objeto != validated_data['objeto']:
        changes.append(
            {'field': 'objeto', 'from': instance.objeto.nome, 'to': validated_data['objeto'].nome})

    if instance.descricao_objeto != validated_data['descricao_objeto']:
        changes.append(
            {'field': 'descricao_objeto', 'from': instance.descricao_objeto, 'to': validated_data['descricao_objeto']})

    return changes


def dif_grupos_de_obrigacoes(grupos_de_obrigacoes_old, grupos_de_obrigacoes_new):
    grupos_de_obrigacoes = []

    # Tratando adição e edição de grupos
    if grupos_de_obrigacoes_old.all().count() <= len(grupos_de_obrigacoes_new):

        for index, grupo_new in enumerate(grupos_de_obrigacoes_new):
            grupo = {}

            try:
                grupo_obrigacao = grupos_de_obrigacoes_old.all().order_by('id')[index]
            except IndexError:
                grupo_obrigacao = None

            if not grupo_obrigacao or grupo_obrigacao.nome != grupo_new['nome']:
                grupo['nome'] = {
                    'from': grupo_obrigacao.nome,
                    'to': grupo_new['nome']}

            itens_obrigacao_old = [
                {'uuid': str(obrigacao.uuid), 'item': obrigacao.item, 'descricao': obrigacao.descricao}
                for obrigacao in grupo_obrigacao.itens_de_obrigacao.all()]
            itens_obrigacao_new = [
                {'item': obrigacao['item'], 'descricao': obrigacao['descricao']}
                for obrigacao in grupo_new['itens_de_obrigacao']]

            grupo['itens_obrigacao'] = {
                'from': itens_obrigacao_old,
                'to': itens_obrigacao_new
            }

            if grupo:
                grupos_de_obrigacoes.append(grupo)

    return grupos_de_obrigacoes


def log_update(instance, validated_data, user=None):
    import json
    from datetime import datetime
    historico = {}
    changes = diff_edital(instance, validated_data)

    if changes:
        historico['updated_at'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        historico['user'] = {'uuid': str(user.uuid), 'email': user.email} if user else user
        historico['action'] = 'UPDATE'
        historico['changes'] = changes

        hist = json.loads(instance.historico) if instance.historico else []
        hist.append(historico)

        instance.historico = json.dumps(hist)
