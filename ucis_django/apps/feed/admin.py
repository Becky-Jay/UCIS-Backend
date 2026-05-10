from django.contrib import admin
from .models import Post, Reaction, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('created_at',)


class ReactionInline(admin.TabularInline):
    model = Reaction
    extra = 0
    readonly_fields = ('created_at',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [ReactionInline, CommentInline]
    list_display = ('title', 'posted_by', 'college', 'created_at')
    search_fields = ('title', 'content', 'posted_by__username')
    readonly_fields = ('created_at',)
