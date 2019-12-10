from rest_framework import serializers


def gestor_e_suplente_devem_ser_diferentes(gestor, suplente):
    if gestor and gestor == suplente:
        raise serializers.ValidationError({'detail': 'Gestor e Suplente devem ser diferentes'})
