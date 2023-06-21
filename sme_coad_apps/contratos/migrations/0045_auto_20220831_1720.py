# Generated by Django 2.2.16 on 2022-08-31 20:20

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0044_anexoimpedimento_impedimento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rescisao',
            name='motivo_rescisao',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('DESCUMPRIMENTO_CLAUSULAS', 'Descumprimento de cláusulas contratuais, especificações, projetos ou prazos.'), ('CUMPRIMENTO_IRREGULAR', 'Cumprimento irregular de cláusulas contratuais, especificações, projetos e prazos.'), ('LENTIDAO_NO_CUMPRIMENTO', 'Lentidão no cumprimento do contrato, levando a Administração a comprovar a impossibilidade da conclusão da obra, do serviço ou do fornecimento, nos prazos estipulados.'), ('ATRASO_INJUSTIFICADO', 'Atraso injustificado no início da obra, serviço ou fornecimento.'), ('PARALISACAO_DO_SERVICO', 'Paralisação da obra, do serviço ou do fornecimento, sem justa causa e prévia comunicação à Administração.'), ('SUBCONTRATACAO_DO_OBJETO', 'Subcontratação total ou parcial do seu objeto, a associação do contratado com outrem, a cessão ou transferência, total ou parcial, bem como a fusão, cisão ou incorporação, não admitidas no edital e no contrato.'), ('DESATENDIMENTO_DAS_DETERMINACOES', 'Desatendimento das determinações regulares da autoridade designada para acompanhar e fiscalizar a sua execução, assim como as de seus superiores.'), ('COMENTIMENTO_DE_FALTAS', 'Cometimento reiterado de faltas na sua execução, anotadas na forma do § 1º do art. 67 da Lei nº 8.666/93.'), ('DECRETACAO_DE_FALENCIA', 'Decretação de falência ou a instauração de insolvência civil.'), ('DISSOLUCAO_OU_FALENCIMENTO', 'Dissolução da sociedade ou o falecimento do contratado.'), ('ALTERACAO_DE_FINALIDADE', 'Alteração social ou modificação da finalidade ou da estrutura da empresa.'), ('INTERESSE_PUBLICO', 'Razões de interesse público, de alta relevância e amplo conhecimento.'), ('SUPRESSAO_DA_ADMINISTACAO', 'Supressão, por parte da Administração, de obras, serviços ou compras, acarretando modificação do valor inicial do contrato além do limite  permitido no § 1º do art. 65 da Lei nº 8.666/93.'), ('SUSPENSAO_DA_EXECUCAO', 'Suspensão da execução do contrato por prazo superior a 120 dias, ou repetidas suspensões que totalizem o mesmo prazo.'), ('ATRASO_DOS_PAGAMENTOS', 'Atraso superior a 90 dias dos pagamentos devidos pela Administração.'), ('NAO_LIBERACAO_ADMINISTRACAO', 'Não liberação, por parte da Administração, de área, local ou objeto para execução de obra, serviço ou fornecimento, nos prazos contratuais, bem como das fontes de materiais naturais especificadas no projeto.'), ('OCORRENCIA_CASO_FORTUITO', 'Ocorrência de caso fortuito ou de força maior, regularmente comprovada, impeditiva da execução do contrato.'), ('DESCUPRIMENTO_DA_LEI', 'Descumprimento do disposto no inciso V do art. 27 da Lei  nº 8.666/93, sem prejuízo das sanções penais cabíveis.')], default=None, max_length=431, null=True),
        ),
    ]