from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Post, Reaction, Comment
from .serializers import PostSerializer, PostCreateSerializer, CommentSerializer, ReactionSerializer


class PostListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        return PostSerializer

    def get_queryset(self):
        return Post.objects.select_related('posted_by').prefetch_related('reactions', 'comments').all()

    def perform_create(self, serializer):
        post = serializer.save(posted_by=self.request.user)
        if self.request.user.role == 'student':
            eng = getattr(self.request.user, 'student_engagement', None)
            if eng:
                eng.posts_created += 1
                eng.save(update_fields=['posts_created'])
        elif self.request.user.role == 'alumni':
            eng = getattr(self.request.user, 'alumni_engagement', None)
            if eng:
                eng.posts_created += 1
                eng.save(update_fields=['posts_created'])

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = PostSerializer(queryset, many=True)
        return Response({'message': 'Feed fetched successfully', 'posts': serializer.data})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        post = Post.objects.select_related('posted_by').prefetch_related('reactions', 'comments').get(pk=serializer.instance.pk)
        return Response({'message': 'Post created successfully', 'post': PostSerializer(post).data}, status=status.HTTP_201_CREATED)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.select_related('posted_by').prefetch_related('reactions', 'comments').all()

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        if post.posted_by != request.user and request.user.role not in ('system_admin', 'college_admin'):
            return Response({'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.posted_by != request.user and request.user.role not in ('system_admin', 'college_admin'):
            return Response({'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def react_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    reaction_type = request.data.get('type', 'like')
    reaction, created = Reaction.objects.update_or_create(
        post=post,
        user=request.user,
        defaults={'reaction_type': reaction_type},
    )
    action = 'added' if created else 'updated'
    return Response({'message': f'Reaction {action}', 'reaction': ReactionSerializer(reaction).data})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_reaction(request, pk):
    post = get_object_or_404(Post, pk=pk)
    Reaction.objects.filter(post=post, user=request.user).delete()
    return Response({'message': 'Reaction removed'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    serializer = CommentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    comment = serializer.save(post=post, user=request.user)
    return Response({'message': 'Comment added', 'comment': CommentSerializer(comment).data}, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, post_id=pk)
    if comment.user != request.user and request.user.role not in ('system_admin', 'college_admin'):
        return Response({'message': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)
    comment.delete()
    return Response({'message': 'Comment deleted'})
