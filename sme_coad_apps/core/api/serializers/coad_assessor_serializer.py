from rest_framework import serializers

from ...models import CoadAssessor


class CoadAssessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoadAssessor
        fields = ('id', 'assessor', 'coad')
