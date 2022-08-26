from auditlog.models import AuditlogHistoryField
from auditlog.registry import auditlog
from django.db import models
from multiselectfield import MultiSelectField

from ...core.models_abstracts import ModeloBase
from .contrato import Contrato


class Intercorrencia(ModeloBase):
    # Tipo Intercorrência
    TIPO_INTERCORRENCIA_SUSPENSAO = 'SUSPENSAO'
    TIPO_INTERCORRENCIA_IMPEDIMENTO = 'IMPEDIMENTO'
    TIPO_INTERCORRENCIA_RESCISAO = 'RESCISAO'

    TIPO_NOMES = {
        TIPO_INTERCORRENCIA_SUSPENSAO: 'Suspensão',
        TIPO_INTERCORRENCIA_IMPEDIMENTO: 'Impedimento',
        TIPO_INTERCORRENCIA_RESCISAO: 'Rescisão',
    }

    TIPO_CHOICES = (
        (TIPO_INTERCORRENCIA_SUSPENSAO, TIPO_NOMES[TIPO_INTERCORRENCIA_SUSPENSAO]),
        (TIPO_INTERCORRENCIA_IMPEDIMENTO, TIPO_NOMES[TIPO_INTERCORRENCIA_IMPEDIMENTO]),
        (TIPO_INTERCORRENCIA_RESCISAO, TIPO_NOMES[TIPO_INTERCORRENCIA_RESCISAO]),
    )

    contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
    tipo_intercorrencia = models.CharField(choices=TIPO_CHOICES, max_length=25)
    data_encerramento = models.DateField('Data de Encerramento', null=True)

    class Meta:
        abstract = True


class Impedimento(Intercorrencia):

    historico = AuditlogHistoryField()
    data_inicial = models.DateField('Data Inicial')
    data_final = models.DateField('Data Final')
    vigencia = models.PositiveSmallIntegerField('vigência', default=0)
    descricao_impedimento = models.TextField('Descrição do Motivo')
    anexo = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.tipo_intercorrencia

    class Meta:
        verbose_name = 'Impedimento'
        verbose_name_plural = 'Impedimentos'


class Suspensao(Intercorrencia):
    # Motivos de Suspensão
    MOTIVO_SUSPENSAO_UNILATERALMENTE_ADMINISTRACAO_PUBLICA = 'UNILATERALMENTE_ADMINISTRACAO_PUBLICA'
    MOTIVO_SUSPENSAO_UNILATERALMENTE_CONTRATADO = 'UNILATERALMENTE_CONTRATADO'
    MOTIVO_SUSPENSAO_CONSENSUALMENTE = 'CONSENSUALMENTE'

    MOTIVO_NOMES = {
        MOTIVO_SUSPENSAO_UNILATERALMENTE_ADMINISTRACAO_PUBLICA: 'Unilateralmente pela Administração Pública',
        MOTIVO_SUSPENSAO_UNILATERALMENTE_CONTRATADO: 'Unilateralmente pelo Contratado',
        MOTIVO_SUSPENSAO_CONSENSUALMENTE: 'Consensualmente',
    }

    MOTIVO_CHOICES = (
        (MOTIVO_SUSPENSAO_UNILATERALMENTE_ADMINISTRACAO_PUBLICA,
         MOTIVO_NOMES[MOTIVO_SUSPENSAO_UNILATERALMENTE_ADMINISTRACAO_PUBLICA]),
        (MOTIVO_SUSPENSAO_UNILATERALMENTE_CONTRATADO, MOTIVO_NOMES[MOTIVO_SUSPENSAO_UNILATERALMENTE_CONTRATADO]),
        (MOTIVO_SUSPENSAO_CONSENSUALMENTE, MOTIVO_NOMES[MOTIVO_SUSPENSAO_CONSENSUALMENTE]),
    )

    historico = AuditlogHistoryField()
    data_inicial = models.DateField('Data Inicial', null=True)
    data_final = models.DateField('Data Final', null=True)
    acrescentar_dias = models.BooleanField(default=False)
    motivo_suspensao = models.CharField(choices=MOTIVO_CHOICES, max_length=50, blank='')
    opcao_suspensao = models.TextField('Opção de Suspensão', blank=True)
    descricao_suspensao = models.TextField('Descrição do Motivo', blank=True)

    @classmethod
    def motivos_suspensao_to_json(cls):
        result = []
        for motivo in cls.MOTIVO_CHOICES:
            choice = {
                'id': motivo[0],
                'nome': motivo[1]
            }
            result.append(choice)
        return result

    def __str__(self):
        return self.tipo_intercorrencia

    class Meta:
        verbose_name = 'Suspensão'
        verbose_name_plural = 'Suspensões'


class Rescisao(Intercorrencia):
    # Motivos de Rescisão
    MOTIVO_RESCISAO_DESCUMPRIMENTO_CLAUSULAS = 'DESCUMPRIMENTO_CLAUSULAS'
    MOTIVO_RESCISAO_CUMPRIMENTO_IRREGULAR = 'CUMPRIMENTO_IRREGULAR'
    MOTIVO_RESCISAO_LENTIDAO_NO_CUMPRIMENTO = 'LENTIDAO_NO_CUMPRIMENTO'
    MOTIVO_RESCISAO_ATRASO_INJUSTIFICADO = 'ATRASO_INJUSTIFICADO'
    MOTIVO_RESCISAO_PARALISACAO_DO_SERVICO = 'PARALISACAO_DO_SERVICO'
    MOTIVO_RESCISAO_SUBCONTRATACAO_DO_OBJETO = 'SUBCONTRATACAO_DO_OBJETO'
    MOTIVO_RESCISAO_DESATENDIMENTO_DAS_DETERMINACOES = 'DESATENDIMENTO_DAS_DETERMINACOES'
    MOTIVO_RESCISAO_COMENTIMENTO_DE_FALTAS = 'COMENTIMENTO_DE_FALTAS'
    MOTIVO_RESCISAO_DECRETACAO_DE_FALENCIA = 'DECRETACAO_DE_FALENCIA'
    MOTIVO_RESCISAO_DISSOLUCAO_OU_FALENCIMENTO = 'DISSOLUCAO_OU_FALENCIMENTO'
    MOTIVO_RESCISAO_ALTERACAO_DE_FINALIDADE = 'ALTERACAO_DE_FINALIDADE'
    MOTIVO_RESCISAO_INTERESSE_PUBLICO = 'INTERESSE_PUBLICO'
    MOTIVO_RESCISAO_SUPRESSAO_DA_ADMINISTACAO = 'SUPRESSAO_DA_ADMINISTACAO'
    MOTIVO_RESCISAO_SUSPENSAO_DA_EXECUCAO = 'SUSPENSAO_DA_EXECUCAO'
    MOTIVO_RESCISAO_ATRASO_DOS_PAGAMENTOS = 'ATRASO_DOS_PAGAMENTOS'
    MOTIVO_RESCISAO_NAO_LIBERACAO_ADMINISTRACAO = 'NAO_LIBERACAO_ADMINISTRACAO'
    MOTIVO_RESCISAO_OCORRENCIA_CASO_FORTUITO = 'OCORRENCIA_CASO_FORTUITO'
    MOTIVO_RESCISAO_DESCUPRIMENTO_DA_LEI = 'DESCUPRIMENTO_DA_LEI'

    MOTIVO_RESCISAO_NOMES = {
        MOTIVO_RESCISAO_DESCUMPRIMENTO_CLAUSULAS: 'Descumprimento de cláusulas contratuais, especificações, '
                                                  'projetos ou prazos.',
        MOTIVO_RESCISAO_CUMPRIMENTO_IRREGULAR: 'Cumprimento irregular de cláusulas contratuais, especificações, '
                                               'projetos e prazos.',
        MOTIVO_RESCISAO_LENTIDAO_NO_CUMPRIMENTO: 'Lentidão no cumprimento do contrato, levando a Administração a '
                                                 'comprovar a impossibilidade da conclusão da obra, do serviço ou '
                                                 'do fornecimento, nos prazos estipulados.',
        MOTIVO_RESCISAO_ATRASO_INJUSTIFICADO: 'Atraso injustificado no início da obra, serviço ou fornecimento.',
        MOTIVO_RESCISAO_PARALISACAO_DO_SERVICO: 'Paralisação da obra, do serviço ou do fornecimento, sem justa causa e '
                                                'prévia comunicação à Administração.',

        MOTIVO_RESCISAO_SUBCONTRATACAO_DO_OBJETO: 'Subcontratação total ou parcial do seu objeto, a associação do '
                                                  'contratado com outrem, a cessão ou transferência, total ou parcial, '
                                                  'bem como a fusão, cisão ou incorporação, não admitidas no edital e'
                                                  ' no contrato.',
        MOTIVO_RESCISAO_DESATENDIMENTO_DAS_DETERMINACOES: 'Desatendimento das determinações regulares da autoridade '
                                                          'designada para acompanhar e fiscalizar a sua execução, assim'
                                                          ' como as de seus superiores.',
        MOTIVO_RESCISAO_COMENTIMENTO_DE_FALTAS: 'Cometimento reiterado de faltas na sua execução, anotadas na forma do '
                                                '§ 1º do art. 67 da Lei nº 8.666/93.',
        MOTIVO_RESCISAO_DECRETACAO_DE_FALENCIA: 'Decretação de falência ou a instauração de insolvência civil.',
        MOTIVO_RESCISAO_DISSOLUCAO_OU_FALENCIMENTO: 'Dissolução da sociedade ou o falecimento do contratado.',
        MOTIVO_RESCISAO_ALTERACAO_DE_FINALIDADE: 'Alteração social ou modificação da finalidade ou da estrutura '
                                                 'da empresa.',
        MOTIVO_RESCISAO_INTERESSE_PUBLICO: 'Razões de interesse público, de alta relevância e amplo conhecimento.',
        MOTIVO_RESCISAO_SUPRESSAO_DA_ADMINISTACAO: 'Supressão, por parte da Administração, de obras, serviços ou '
                                                   'compras, acarretando modificação do valor inicial do contrato '
                                                   'além do limite  permitido no § 1º do art. 65 da Lei nº 8.666/93.',
        MOTIVO_RESCISAO_SUSPENSAO_DA_EXECUCAO: 'Suspensão da execução do contrato por prazo superior a 120 dias, ou '
                                               'repetidas suspensões que totalizem o mesmo prazo." Houve alteração em '
                                               'relação ao previsto no protótipo.',
        MOTIVO_RESCISAO_ATRASO_DOS_PAGAMENTOS: 'Atraso superior a 90 dias dos pagamentos devidos pela Administração.',
        MOTIVO_RESCISAO_NAO_LIBERACAO_ADMINISTRACAO: 'Não liberação, por parte da Administração, de área, local ou'
                                                     ' objeto para execução de obra, serviço ou fornecimento, nos '
                                                     'prazos contratuais, bem como das fontes de materiais naturais'
                                                     ' especificadas no projeto.',
        MOTIVO_RESCISAO_OCORRENCIA_CASO_FORTUITO: 'Ocorrência de caso fortuito ou de força maior, regularmente '
                                                  'comprovada, impeditiva da execução do contrato.',
        MOTIVO_RESCISAO_DESCUPRIMENTO_DA_LEI: 'Descumprimento do disposto no inciso V do art. 27 da Lei  nº 8.666/93, '
                                              'sem prejuízo das sanções penais cabíveis.'
    }
    MOTIVO_RESCICAO_CHOICES = (
        (MOTIVO_RESCISAO_DESCUMPRIMENTO_CLAUSULAS, MOTIVO_RESCISAO_NOMES[MOTIVO_RESCISAO_DESCUMPRIMENTO_CLAUSULAS]),
        (MOTIVO_RESCISAO_CUMPRIMENTO_IRREGULAR, MOTIVO_RESCISAO_NOMES[MOTIVO_RESCISAO_CUMPRIMENTO_IRREGULAR]),
        (MOTIVO_RESCISAO_LENTIDAO_NO_CUMPRIMENTO, MOTIVO_RESCISAO_NOMES[MOTIVO_RESCISAO_LENTIDAO_NO_CUMPRIMENTO]),
        (MOTIVO_RESCISAO_ATRASO_INJUSTIFICADO, MOTIVO_RESCISAO_NOMES[MOTIVO_RESCISAO_ATRASO_INJUSTIFICADO]),
        (MOTIVO_RESCISAO_PARALISACAO_DO_SERVICO, MOTIVO_RESCISAO_NOMES[MOTIVO_RESCISAO_PARALISACAO_DO_SERVICO]),
        (MOTIVO_RESCISAO_SUBCONTRATACAO_DO_OBJETO, MOTIVO_RESCISAO_NOMES[MOTIVO_RESCISAO_SUBCONTRATACAO_DO_OBJETO]),
        (MOTIVO_RESCISAO_DESATENDIMENTO_DAS_DETERMINACOES,
         MOTIVO_RESCISAO_NOMES[MOTIVO_RESCISAO_DESATENDIMENTO_DAS_DETERMINACOES]),
        (MOTIVO_RESCISAO_COMENTIMENTO_DE_FALTAS, MOTIVO_RESCISAO_NOMES[MOTIVO_RESCISAO_COMENTIMENTO_DE_FALTAS]),
        (MOTIVO_RESCISAO_DECRETACAO_DE_FALENCIA, MOTIVO_RESCISAO_NOMES[MOTIVO_RESCISAO_DECRETACAO_DE_FALENCIA]),
        (MOTIVO_RESCISAO_DISSOLUCAO_OU_FALENCIMENTO, MOTIVO_RESCISAO_NOMES[MOTIVO_RESCISAO_DISSOLUCAO_OU_FALENCIMENTO]),
        (MOTIVO_RESCISAO_ALTERACAO_DE_FINALIDADE, MOTIVO_RESCISAO_NOMES[MOTIVO_RESCISAO_ALTERACAO_DE_FINALIDADE]),
        (MOTIVO_RESCISAO_INTERESSE_PUBLICO, MOTIVO_RESCISAO_NOMES[MOTIVO_RESCISAO_INTERESSE_PUBLICO]),
        (MOTIVO_RESCISAO_SUPRESSAO_DA_ADMINISTACAO, MOTIVO_RESCISAO_NOMES[MOTIVO_RESCISAO_SUPRESSAO_DA_ADMINISTACAO]),
        (MOTIVO_RESCISAO_SUSPENSAO_DA_EXECUCAO, MOTIVO_RESCISAO_NOMES[MOTIVO_RESCISAO_SUSPENSAO_DA_EXECUCAO]),
        (MOTIVO_RESCISAO_ATRASO_DOS_PAGAMENTOS, MOTIVO_RESCISAO_NOMES[MOTIVO_RESCISAO_ATRASO_DOS_PAGAMENTOS]),
        (MOTIVO_RESCISAO_NAO_LIBERACAO_ADMINISTRACAO,
         MOTIVO_RESCISAO_NOMES[MOTIVO_RESCISAO_NAO_LIBERACAO_ADMINISTRACAO]),
        (MOTIVO_RESCISAO_OCORRENCIA_CASO_FORTUITO, MOTIVO_RESCISAO_NOMES[MOTIVO_RESCISAO_OCORRENCIA_CASO_FORTUITO]),
        (MOTIVO_RESCISAO_DESCUPRIMENTO_DA_LEI, MOTIVO_RESCISAO_NOMES[MOTIVO_RESCISAO_DESCUPRIMENTO_DA_LEI]),
    )

    historico = AuditlogHistoryField()
    motivo_rescisao = MultiSelectField(choices=MOTIVO_RESCICAO_CHOICES, default=None, null=True)
    data_rescisao = models.DateField('Data Rescisão', null=True)

    @classmethod
    def motivos_rescisao_to_json(cls):
        result = []
        for motivo in cls.MOTIVO_RESCICAO_CHOICES:
            choice = {
                'id': motivo[0],
                'nome': motivo[1]
            }
            result.append(choice)
        return result

    def __str__(self):
        return self.tipo_intercorrencia

    class Meta:
        verbose_name = 'Rescisão'
        verbose_name_plural = 'Rescisões'


auditlog.register(Suspensao)
auditlog.register(Rescisao)
