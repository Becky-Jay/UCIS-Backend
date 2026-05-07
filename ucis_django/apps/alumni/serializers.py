from rest_framework import serializers
from apps.users.serializers import UserSummarySerializer
from .models import AlumniProfile


class AlumniProfileSerializer(serializers.ModelSerializer):
    user = UserSummarySerializer(read_only=True)

    class Meta:
        model = AlumniProfile
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')


class AlumniProfileCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlumniProfile
        exclude = ('user', 'created_at', 'updated_at')
