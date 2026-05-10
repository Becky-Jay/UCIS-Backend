from rest_framework import serializers
from .models import Deadline, AlmanacEvent


class DeadlineSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Deadline
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')


class AlmanacEventSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = AlmanacEvent
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')
