from rest_framework import serializers
from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    performed_by_name = serializers.CharField(source='performed_by.username', read_only=True, default=None)

    class Meta:
        model = AuditLog
        fields = '__all__'
        read_only_fields = ('timestamp',)
