from django.contrib import admin
from .models import News, NewsMedia


class NewsMediaInline(admin.TabularInline):
    model = NewsMedia
    extra = 1


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    inlines = [NewsMediaInline]
    list_display = ('title', 'category', 'created_by', 'is_published', 'is_archived', 'created_at')
    list_filter = ('category', 'is_published', 'is_archived')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')
