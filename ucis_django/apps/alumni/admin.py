from django.contrib import admin
from .models import AlumniProfile


@admin.register(AlumniProfile)
class AlumniProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'graduation_year', 'company', 'position', 'industry', 'is_verified', 'joined_mentorship')
    list_filter = ('is_verified', 'joined_mentorship', 'industry')
    search_fields = ('user__username', 'company', 'position')
    readonly_fields = ('created_at', 'updated_at')
