from .models.coad_assessor import CoadAssessor
from .models.servidor import Servidor


def limpa_assessores_coad():
    CoadAssessor.limpa_assessores()


def update_assessores_coad(assessores):
    limpa_assessores_coad()
    CoadAssessor.append_assessores(assessores)


def limpa_servidores_nucleo(nucleo):
    Servidor.limpa_servidores(nucleo=nucleo)


def update_servidores_nucleo(servidores, nucleo):
    limpa_servidores_nucleo(nucleo=nucleo)
    Servidor.append_servidores(nucleo=nucleo, servidores=servidores)
