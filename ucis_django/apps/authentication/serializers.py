from rest_framework import serializers
from apps.users.models import User, UserProfile, Education, WorkExperience, Expertise, Achievement


class ProfileInputSerializer(serializers.Serializer):
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    department = serializers.CharField(required=False, allow_blank=True)
    graduationYear = serializers.IntegerField(required=False, allow_null=True)
    registrationNumber = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    profilePicture = serializers.URLField(required=False, allow_blank=True)
    mentorshipAvailability = serializers.BooleanField(required=False, default=False)


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
    role = serializers.ChoiceField(choices=['student', 'alumni', 'college_admin', 'system_admin'])
    college = serializers.CharField(required=False, allow_blank=True)
    profile = ProfileInputSerializer()
    interests = serializers.ListField(child=serializers.CharField(), required=False, default=list)
    fcmTokens = serializers.ListField(child=serializers.CharField(), required=False, default=list)

    def validate(self, data):
        role = data.get('role')
        college = data.get('college', '')
        if role in ('student', 'college_admin') and not college:
            raise serializers.ValidationError({'college': 'College is required for this role.'})
        return data

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists.')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists.')
        return value

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        interests = validated_data.pop('interests', [])
        fcm_tokens = validated_data.pop('fcmTokens', [])
        password = validated_data.pop('password')
        role = validated_data['role']

        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            role=role,
            college=validated_data.get('college', ''),
            fcm_tokens=fcm_tokens,
        )
        user.set_password(password)
        user.save()

        notification_prefs = {
            'events': True,
            'news': True,
            'announcements': True,
            'mentorship': True,
            'opportunities': True,
            'social': True,
        }

        UserProfile.objects.filter(user=user).update(
            first_name=profile_data.get('firstName', ''),
            last_name=profile_data.get('lastName', ''),
            department=profile_data.get('department', ''),
            graduation_year=profile_data.get('graduationYear'),
            registration_number=profile_data.get('registrationNumber', ''),
            phone=profile_data.get('phone', ''),
            bio=profile_data.get('bio', ''),
            profile_picture=profile_data.get('profilePicture', ''),
            mentorship_availability=profile_data.get('mentorshipAvailability', False) if role == 'alumni' else False,
            interests=interests,
            notification_preferences=notification_prefs,
        )

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(min_length=8)


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(min_length=8, write_only=True)


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()
