import json


def serializa_historico(log_entry):
    historico = []
    for reg in log_entry.all():
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
        registro['created_at'] = reg.timestamp.strftime('%m/%d/%Y %H:%M:%S')
        if reg.action == 0:
            registro['action'] = 'CREATE'
        elif reg.action == 1:
            registro['action'] = 'UPDATE'

        historico.append(registro)

    return historico
