from rest_framework import serializers
from .models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    reviewed_by_name = serializers.CharField(source='reviewed_by.username', read_only=True, default=None)

    class Meta:
        model = Feedback
        fields = '__all__'
        read_only_fields = ('user', 'status', 'admin_response', 'reviewed_by', 'created_at', 'updated_at')


class FeedbackAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ('status', 'admin_response', 'reviewed_by')
