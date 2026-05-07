from rest_framework import serializers
from .models import MentorshipRequest


class MentorshipRequestSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.username', read_only=True)
    alumni_name = serializers.CharField(source='alumni.username', read_only=True)

    class Meta:
        model = MentorshipRequest
        fields = '__all__'
        read_only_fields = ('student', 'created_at', 'updated_at')
