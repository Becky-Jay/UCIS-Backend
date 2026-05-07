from rest_framework import serializers
from .models import (
    User, UserProfile, Education, WorkExperience,
    Expertise, Achievement, Relationship,
    StudentEngagement, AlumniEngagement,
    SystemAdminEngagement, CollegeAdminEngagement,
)


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        exclude = ('user',)


class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        exclude = ('user',)


class ExpertiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expertise
        exclude = ('user',)


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        exclude = ('user',)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ('user', 'id')


class StudentEngagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentEngagement
        exclude = ('user', 'id')


class AlumniEngagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlumniEngagement
        exclude = ('user', 'id')


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    education = EducationSerializer(many=True, read_only=True)
    work_experience = WorkExperienceSerializer(many=True, read_only=True)
    expertise = ExpertiseSerializer(many=True, read_only=True)
    achievements = AchievementSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'role', 'college',
            'is_active', 'last_active', 'fcm_tokens',
            'profile', 'education', 'work_experience', 'expertise', 'achievements',
        )


class UserSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing users."""
    first_name = serializers.CharField(source='profile.first_name', read_only=True)
    last_name = serializers.CharField(source='profile.last_name', read_only=True)
    profile_picture = serializers.URLField(source='profile.profile_picture', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'college', 'is_active', 'first_name', 'last_name', 'profile_picture')


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ('user',)


class UpdateUserSerializer(serializers.ModelSerializer):
    profile = UpdateProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'college', 'is_active', 'fcm_tokens', 'profile')
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'role': {'required': False},
        }

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance
