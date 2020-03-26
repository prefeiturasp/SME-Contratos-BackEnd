from auditlog.models import LogEntry
from rest_framework import serializers


class HistoricoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogEntry
        fields = '__all__'
