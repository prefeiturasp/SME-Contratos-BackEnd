import pytest
from rest_framework import serializers

from sme_coad_apps.users.api.validations.usuario_validations import senha_nao_pode_ser_nulo, senhas_devem_ser_iguais

pytestmark = pytest.mark.django_db


def test_senhas_devem_ser_iguais():
    pass1 = '123456'
    pass2 = '1234567'
    esperado = 'Senhas informadas devem ser iguais'
    with pytest.raises(serializers.ValidationError, match=esperado):
        senhas_devem_ser_iguais(pass1, pass2)
    assert senhas_devem_ser_iguais(pass1, pass1) is None


def test_campos_vazios_devem_ser_preenchidos():
    campo1 = 'Senha'
    valor1 = '123456'
    valor2 = ''
    valor3 = None
    esperado = f'O Campo {campo1} deve ser preenchido'
    with pytest.raises(serializers.ValidationError, match=esperado):
        senha_nao_pode_ser_nulo(valor2, campo1)
        senha_nao_pode_ser_nulo(valor3, campo1)

    assert senha_nao_pode_ser_nulo(valor1, campo1) is None
