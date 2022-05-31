import json


def serializa_historico(log_entry):
    historico = []
    for reg in log_entry.all().reverse():
        registro = {}

        mudancas = json.loads(reg.changes)
        changes = []
        for key in mudancas.keys():
            newChange = {}
            newChange['field'] = key
            newChange['from'] = mudancas[key][0]
            newChange['to'] = mudancas[key][1]
            changes.append(newChange)

        registro['changes'] = changes
        registro['user'] = {
            'email': reg.actor.email,
            'uuid': str(reg.actor.uuid)
        } if reg.actor else None
        data = reg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        if reg.action == 0:
            registro['created_at'] = data
            registro['action'] = 'CREATE'
        elif reg.action == 1:
            registro['updated_at'] = data
            registro['action'] = 'UPDATE'

        historico.append(registro)

    return historico
