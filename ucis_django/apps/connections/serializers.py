from rest_framework import serializers
from apps.users.serializers import UserSummarySerializer
from .models import Connection, Message


class ConnectionSerializer(serializers.ModelSerializer):
    sender_info = UserSummarySerializer(source='sender', read_only=True)
    receiver_info = UserSummarySerializer(source='receiver', read_only=True)

    class Meta:
        model = Connection
        fields = '__all__'
        read_only_fields = ('sender', 'created_at', 'updated_at')


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    recipient_name = serializers.CharField(source='recipient.username', read_only=True)

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ('sender', 'is_read', 'read_at', 'created_at')
