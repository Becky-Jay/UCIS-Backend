from django.contrib import admin
from .models import ChatSession, ChatMessage


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    inlines = [ChatMessageInline]
    list_display = ('id', 'user', 'status', 'started_at', 'ended_at')
    list_filter = ('status',)
    search_fields = ('user__username',)
    readonly_fields = ('started_at',)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'sender_type', 'message_text', 'created_at')
    list_filter = ('sender_type',)
    readonly_fields = ('created_at',)
