def convert_contrato_unidade_to_json(unidades_contrato):
    unidade_contrato_lista = []
    for unidade in unidades_contrato:
        unidade_contrato_lista.append({
            'termo_contrato': unidade.contrato.termo_contrato,
            'codigo_eol': unidade.unidade.codigo_eol,
            'tipo_unidade': unidade.unidade.tipo_unidade,
            'equipamento': unidade.unidade.equipamento,
            'dre': unidade.dre_lote,
            'lote': unidade.lote
        })
    return unidade_contrato_lista
