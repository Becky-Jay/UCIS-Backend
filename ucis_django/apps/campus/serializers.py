from rest_framework import serializers
from .models import CampusLocation


class CampusLocationSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.username', read_only=True, default=None)
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = CampusLocation
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')
