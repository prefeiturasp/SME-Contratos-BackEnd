import datetime

from auditlog.models import LogEntry


def serializa_historico(log_entry, lista=None, valor=None):
    historico = []
    registro, objetos, reg, action = {}, [], None, 'U'

    if log_entry:
        lista = log_entry.all().reverse()
        valor = lista[0].object_repr
    for reg in lista:
        if reg.object_repr == valor:
            registro = {}
            mudancas = reg.changes_dict
            changes = []
            for key in mudancas.keys():
                newChange = {}
                newChange['field'] = key
                newChange['from'] = mudancas[key][0]
                newChange['to'] = mudancas[key][1]
                changes.append(newChange)
            registro['changes'] = changes
            action = 'C' if reg.action == 0 else 'U'
        else:
            objetos = objetos_historico(reg, objetos)

        if objetos:
            registro['objetos'] = objetos
        registro['user'] = {
            'email': reg.actor.email,
            'uuid': str(reg.actor.uuid)
        } if reg.actor else None
        data = reg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        if action == 'C':
            registro['created_at'] = data
            registro['action'] = 'CREATE'
        else:
            registro['updated_at'] = data
            registro['action'] = 'UPDATE'

        if log_entry:
            historico.append(registro)
        else:
            historico = registro
    return historico


def objetos_historico(reg, objetos):
    objeto = {}
    if reg.action == 0:
        for field in reg.changes_dict:
            objeto[field] = reg.changes_dict[field][1]
        objeto['situacao'] = 'CRIADO'
        objetos.append(objeto)
    elif reg.action == 2:
        for field in reg.changes_dict:
            objeto[field] = reg.changes_dict[field][0]
        objeto['situacao'] = 'EXCLUÍDO'
        objetos.append(objeto)
    return objetos


def registro_historico(log_entry, lista, valor):
    # Para cara lista de logs, verifica e cria changes e objetos
    registro, objetos, reg, action = {}, [], None, 'U'
    for reg in lista:
        if reg.object_repr == valor:
            mudancas = reg.changes_dict
            changes = []
            for key in mudancas.keys():
                newChange = {}
                newChange['field'] = key
                newChange['from'] = mudancas[key][0]
                newChange['to'] = mudancas[key][1]
                changes.append(newChange)
            registro['changes'] = changes
            if reg.action == 0:
                action = 'C'
        else:
            objetos = objetos_historico(reg, objetos)

    if objetos:
        registro['objetos'] = objetos

    registro['user'] = {
        'email': reg.actor.email,
        'uuid': str(reg.actor.uuid)
    } if reg.actor else None
    data = reg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    if action == 'C':
        registro['created_at'] = data
        registro['action'] = 'CREATE'
    else:
        registro['updated_at'] = data
        registro['action'] = 'UPDATE'
    return registro


def serializa_historico_objetos(log_entry, valor=None):
    historico = []
    logs = LogEntry.objects.all().reverse()

    # query obtém todos os logs para aquela entidade
    query = logs.filter(object_repr__contains=valor)

    # todos os logs são agrupados de acordo com a hora e usuário que o criaram
    grupos, lista = [], []
    total = query.count()
    for n in range(0, total):
        if n == 0:
            lista.append(query[0])
        else:
            tempo = query[n - 1].timestamp
            t1 = tempo - datetime.timedelta(0, 2)
            t2 = tempo + datetime.timedelta(0, 2)
            user = query[n - 1].actor
            if t1 < query[n].timestamp < t2 and query[n].actor == user:
                lista.append(query[n])
            else:
                grupos.append(lista)
                lista = [query[n]]
    grupos.append(lista)
    for lista in grupos:
        registro = serializa_historico(None, lista, valor)

        historico.append(registro)
    return historico
