from rest_framework import serializers, status

from django.contrib.auth import get_user_model


def senhas_devem_ser_iguais(senha1, senha2):
    if senha1 != senha2:
        raise serializers.ValidationError({'detail': 'Senhas informadas devem ser iguais'})


def registro_funcional_deve_existir(registro_funcional):
    user = get_user_model()
    usuario = user.objects.filter(username=registro_funcional).exists()
    if not usuario:
        raise serializers.ValidationError({'detail': 'Registro Funcional não foi encontrado'})


def senha_nao_pode_ser_nulo(senha, campo='Senha'):
    if senha is None or senha == 'string':
        raise serializers.ValidationError({'detail': 'O Campo {} deve ser preenchido'.format(campo)})


def usuario_ja_foi_validado(registro_funcional):
    user = get_user_model()
    usuario = user.objects.get(username=registro_funcional)
    if usuario.validado:
        raise serializers.ValidationError({'detail': 'O usuário já foi validado'})
