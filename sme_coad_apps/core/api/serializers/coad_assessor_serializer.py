from django.contrib.auth import get_user_model
from rest_framework import serializers

from ...models import CoadAssessor
from ....users.api.serializers.usuario_serializer import UsuarioLookUpSerializer

user_model = get_user_model()


class CoadAssessorSerializer(serializers.ModelSerializer):
    assessor = UsuarioLookUpSerializer()

    class Meta:
        model = CoadAssessor
        fields = ('id', 'assessor', 'coad')


class CoadAssessorCreateSerializer(serializers.ModelSerializer):
    assessor = serializers.SlugRelatedField(
        slug_field='username',
        required=False,
        queryset=user_model.objects.all()
    )

    class Meta:
        model = CoadAssessor
        fields = ('id', 'assessor', 'coad')
