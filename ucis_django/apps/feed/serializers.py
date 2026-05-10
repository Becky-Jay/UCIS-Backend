from rest_framework import serializers
from .models import Post, Reaction, Comment, Story


class CommentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'user_name', 'content', 'created_at')
        read_only_fields = ('user', 'created_at')


class ReactionSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Reaction
        fields = ('id', 'user', 'user_name', 'reaction_type', 'created_at')
        read_only_fields = ('user', 'created_at')


class PostSerializer(serializers.ModelSerializer):
    reactions = ReactionSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    posted_by_name = serializers.CharField(source='posted_by.username', read_only=True)
    reaction_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('posted_by', 'created_at')

    def get_reaction_count(self, obj):
        return obj.reactions.count()

    def get_comment_count(self, obj):
        return obj.comments.count()


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'content', 'college', 'target_roles', 'tags')


class StorySerializer(serializers.ModelSerializer):
    posted_by_name = serializers.CharField(source='posted_by.username', read_only=True)
    view_count = serializers.SerializerMethodField()
    has_viewed = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = '__all__'
        read_only_fields = ('posted_by', 'viewers', 'created_at')

    def get_view_count(self, obj):
        return obj.viewers.count()

    def get_has_viewed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.viewers.filter(pk=request.user.pk).exists()
        return False
