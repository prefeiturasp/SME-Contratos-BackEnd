[![Maintainability](https://api.codeclimate.com/v1/badges/ad33daa97c71f74ad579/maintainability)](https://codeclimate.com/github/prefeiturasp/SME-Contratos-BackEnd/maintainability)

[![Test Coverage](https://api.codeclimate.com/v1/badges/ad33daa97c71f74ad579/test_coverage)](https://codeclimate.com/github/prefeiturasp/SME-Contratos-BackEnd/test_coverage)

SME-COAD-BackEnd
========

Sistema de gestão da Coordenadoria de Administração, Finanças e Infraestrutura (COAD) da Secretaria de Educação da cidade de São Paulo.

License: MIT

Versão: 0.5.0

## Release Notes
### 0.5.0 - 09/12/2019 - Sprint 5
* Cadastro de Modelos de Ateste
* Duplicar um Modelo de Ateste
* Registro de fiscais e suplentes de um contrato

### 0.4.0 - 22/11/2019 - Sprint 4
* Cadastro único de contratos
* Consulta e Edição de Termos de Contrato
* Notificações por e-mail de atribuição de contrato
* Notificações por e-mail e tela de vencimento de contratos
* Cadastro de Obrigações Contratuais
* Configuração de Parâmetros Globais de alertas de vencimento de contrato.
### 0.3 - 04/11/2019 - Sprint 3
* Consulta de detalhes de um contrato
* Atribuição de um contrato a um gestor e suplente
* Designação de cargos COAD, Divisões e Núcleos

### 0.2 - 18/10/2019 - Sprint 2
* Consulta de contratos
* Painel de seleção de contratos
* Busca avançada de contratos
* Registro de histórico de alterações em um contrato

### 0.1 - 30/09/2019 - Sprint 1
* Importação de planilha de contratos
* Funcionalidades de login
* Redefinição de senha no primeiro acesso


### Para desenvolver

1.  Clone o repositório.
2.  Crie um Virtualenv com Python 3.6
3.  Ative o Virtualenv.
4.  Instale as dependências.
5.  Configure a instância com o .env
6.  Execute os testes.
7.  Faça um Pull Request com o seu desenvolvimento

```console
git clone https://github.com/prefeiturasp/SME-Contratos-BackEnd.git backend-coad
cd backend-coad
python -m venv .venv
source .venv/bin/activate
pip install -r requirements\local.txt
cp env_sample .env
pytest
```

### Tema do Admin
Para instalar o tema do Admin

```console
python manage.py loaddata admin_interface_theme_foundation.json
```
