from rest_framework import serializers
from .models import News, NewsMedia


class NewsMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsMedia
        fields = ('id', 'url', 'media_type')


class NewsSerializer(serializers.ModelSerializer):
    media = NewsMediaSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = News
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')
