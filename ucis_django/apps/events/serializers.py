from rest_framework import serializers
from .models import Event, EventMedia


class EventMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventMedia
        fields = ('id', 'url', 'media_type')


class EventSerializer(serializers.ModelSerializer):
    media = EventMediaSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    attendee_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at', 'attendees')

    def get_attendee_count(self, obj):
        return obj.attendees.count()
