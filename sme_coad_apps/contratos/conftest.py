import datetime

import pytest
from faker import Faker
from model_mommy import mommy

from sme_coad_apps.contratos.models import (
    Aditamento,
    Ata,
    Edital,
    Empresa,
    Objeto,
    Produto,
    Rescisao,
    Suspensao,
    UnidadeDeMedida
)
from sme_coad_apps.contratos.models.ata import ProdutosAta
from sme_coad_apps.users.models import User


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def contrato():
    mommy.make(User,
               username='1111111',
               nome='Galvão Bueno')
    mommy.make(User,
               username='1234567',
               nome='Calvin Feitosa')
    mommy.make('Unidade',
               codigo_eol='108101')
    mommy.make('objeto',
               nome='Teste objeto',
               uuid='7baa3356-599f-4627-9fed-832ee888de14')
    return mommy.make('Contrato',
                      uuid='d0260b07-4ed3-4741-8844-c5c3a9279f55')


@pytest.fixture
def authencticated_client(client, django_user_model):
    fake = Faker()
    username = fake.user_name()
    password = fake.text()
    u = django_user_model.objects.create_user(username=username, password=password)
    u.validado = True
    u.save()
    client.login(username=username, password=password)
    return client


@pytest.fixture
def fake_user(client, django_user_model):
    username = 'teste'
    password = 'teste'
    nome = 'teste'
    email = 'teste@teste.com'
    user = django_user_model.objects.create_user(username=username, password=password, validado=True, nome=nome,
                                                 email=email)
    client.login(username=username, password=password)
    return user


@pytest.fixture
def colunas_contrato(fake_user):
    return mommy.make('ColunasContrato',
                      uuid='d0260b07-4ed3-4741-8844-c5c3a9279f55',
                      usuario=fake_user,
                      colunas_array=[{
                          'field': 'termo_contrato',
                          'header': 'TC'
                      }, {
                          'field': 'processo',
                          'header': 'Processo'
                      }
                      ])


@pytest.fixture
def edital(gestor, suplente):
    return mommy.make(Edital, numero='0123456', processo='6543210', status=Edital.ATIVO,
                      tipo_contratacao=Edital.TIPO_LICITACAO, subtipo='esse é um subtipo',
                      data_homologacao=datetime.date(2023, 1, 1), objeto=mommy.make(Objeto),
                      descricao_objeto='essa é uma descrição do objeto'
                      )


@pytest.fixture
def ata(empresa):
    return mommy.make(Ata, numero='0123456/2022',
                      vigencia=15,
                      status=Ata.ATIVA,
                      data_assinatura=datetime.date(2023, 1, 1),
                      data_encerramento=datetime.date(2023, 1, 15),
                      edital=mommy.make(Edital),
                      empresa=empresa,
                      unidade_vigencia=Ata.UNIDADE_VIGENCIA_DIAS
                      )


@pytest.fixture
def produtos_ata(ata):
    return mommy.make(ProdutosAta, ata=ata,
                      produto=mommy.make(Produto),
                      quantidade_total=10.0,
                      valor_unitario=10.0,
                      valor_total=100.0,
                      )


@pytest.fixture
def empresa():
    return mommy.make(Empresa,
                      cnpj='21256564000160',
                      razao_social='Empresa Teste LTDA',
                      tipo_servico=Empresa.FORNECEDOR,
                      tipo_fornecedor=Empresa.CONVENCIONAL,
                      situacao=Empresa.SITUACAO_ATIVA,
                      cep='04284000',
                      endereco='Rua América',
                      bairro='Vila Moinho',
                      cidade='São Paulo',
                      estado='São Paulo',
                      numero='100',
                      complemento=''
                      )


@pytest.fixture
def produto():
    return mommy.make(Produto,
                      unidade_medida=mommy.make(UnidadeDeMedida),
                      nome='Produto Teste',
                      categoria=Produto.CATEGORIA_ALIMENTO,
                      situacao=Produto.SITUACAO_ATIVO,
                      grupo_alimentar=Produto.GRUPO_ALIMENTAR_SECOS,
                      durabilidade=Produto.DURABILIDADE_NAO_PERECIVEL,
                      armazenabilidade=Produto.ARMAZENABILIDADE_ARMAZENAVEL
                      )


@pytest.fixture
def dotacao_orcamentaria():
    return mommy.make('DotacaoOrcamentaria',
                      orgao='99',
                      unidade='88',
                      funcao='77',
                      subfuncao='666',
                      programa='5555',
                      projeto_atividade='4.444',
                      conta_despesa='33333333',
                      fonte='22'
                      )


@pytest.fixture
def aditamento(contrato):
    return mommy.make(Aditamento, termo_aditivo='12345/2022',
                      objeto_aditamento=[Aditamento.OBJETO_PRORROGACAO_VIGENCIA_CONTRATUAL],
                      data_inicial=datetime.date(2023, 1, 1),
                      data_final=datetime.date(2023, 1, 15),
                      valor_mensal_atualizado=10000.0,
                      valor_total_atualizado=200000.0,
                      valor_aditamento=100000.0,
                      contrato=contrato,
                      razoes_aditamento='testando aditamento'
                      )


@pytest.fixture
def rescisao(contrato):
    return mommy.make(Rescisao, contrato=contrato,
                      tipo_intercorrencia=Rescisao.TIPO_INTERCORRENCIA_RESCISAO,
                      data_rescisao=datetime.date(2022, 8, 25),
                      motivo_rescisao=[Rescisao.MOTIVO_RESCISAO_DESCUMPRIMENTO_CLAUSULAS,
                                       Rescisao.MOTIVO_RESCISAO_LENTIDAO_NO_CUMPRIMENTO],
                      )


@pytest.fixture
def suspensao(contrato):
    return mommy.make(Suspensao, contrato=contrato,
                      tipo_intercorrencia=Suspensao.TIPO_INTERCORRENCIA_SUSPENSAO,
                      data_inicial=datetime.date(2022, 1, 1),
                      data_final=datetime.date(2022, 1, 15),
                      acrescentar_dias=True,
                      motivo_suspensao=Suspensao.MOTIVO_SUSPENSAO_UNILATERALMENTE_ADMINISTRACAO_PUBLICA,
                      opcao_suspensao='Conveniência da Administração Pública',
                      descricao_suspensao='testando intercorrência'
                      )
