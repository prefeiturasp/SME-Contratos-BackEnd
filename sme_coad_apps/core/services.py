from .models.coad_assessor import CoadAssessor


def limpa_assessores_coad():
    CoadAssessor.limpa_assessores()


def update_assessores_coad(assessores):
    limpa_assessores_coad()
    CoadAssessor.append_assessores(assessores)
