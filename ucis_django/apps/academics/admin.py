from django.contrib import admin
from .models import Deadline, AlmanacEvent


@admin.register(Deadline)
class DeadlineAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'college', 'department', 'deadline_date', 'is_active')
    list_filter = ('category', 'college', 'is_active')
    search_fields = ('title', 'course', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(AlmanacEvent)
class AlmanacEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'academic_year', 'start_date', 'end_date', 'is_public')
    list_filter = ('category', 'academic_year', 'is_public')
    search_fields = ('title', 'description', 'academic_year')
    readonly_fields = ('created_at', 'updated_at')
