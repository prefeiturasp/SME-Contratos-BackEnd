import datetime

from config import celery_app

from .models import RequisicaoApiSofi
from .utils import SOFIService

ANO_CORRENTE = datetime.date.today().year
MES_CORRENTE = datetime.date.today().month


@celery_app.task(soft_time_limit=1000, time_limit=1200)
def testes_api_sofi():
    despesa = RequisicaoApiSofi.criar_requisicao('despesas')
    result_despesa = SOFIService.get_informacoes_despesas(ANO_CORRENTE, MES_CORRENTE)
    if result_despesa:
        despesa.status = RequisicaoApiSofi.SUCESSO
        despesa.resultado = result_despesa
    else:
        despesa.status = RequisicaoApiSofi.ERRO
    despesa.save()

    empenho = RequisicaoApiSofi.criar_requisicao('empenhos')
    result_empenho = SOFIService.get_informacoes_empenhos(ANO_CORRENTE, MES_CORRENTE)
    if result_empenho:
        empenho.status = RequisicaoApiSofi.SUCESSO
        empenho.resultado = result_empenho
    else:
        empenho.status = RequisicaoApiSofi.ERRO
    empenho.save()

    contrato = RequisicaoApiSofi.criar_requisicao('contratos')
    result_contrato = SOFIService.get_informacoes_contratos(ANO_CORRENTE)
    if result_contrato:
        contrato.status = RequisicaoApiSofi.SUCESSO
        contrato.resultado = result_contrato
    else:
        contrato.status = RequisicaoApiSofi.ERRO
    contrato.save()

    dispesas_por_credor = RequisicaoApiSofi.criar_requisicao('dispesasCredor')
    result_dispesas_por_credor = SOFIService.get_informacoes_dispesas_por_credor(ANO_CORRENTE, MES_CORRENTE)
    if result_dispesas_por_credor:
        dispesas_por_credor.status = RequisicaoApiSofi.SUCESSO
        dispesas_por_credor.resultado = result_dispesas_por_credor
    else:
        dispesas_por_credor.status = RequisicaoApiSofi.ERRO
    dispesas_por_credor.save()
