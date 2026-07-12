from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.models import Comment, Post
from src.serializers.post_serializers import CommentSerializer, PostSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user_posts(request):
    posts = Post.objects.filter(user=request.user)
    return Response({
        'status': 'success',
        'message': 'User posts fetched successfully',
        'data': {'posts': PostSerializer(posts, many=True).data},
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_posts(request):
    posts = Post.objects.select_related(
        'user').prefetch_related('comments__user').all()
    return Response({
        'status': 'success',
        'message': 'Posts fetched successfully',
        'data': {'posts': PostSerializer(posts, many=True).data},
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_post_by_id(request, pk):
    try:
        post = Post.objects.select_related(
            'user').prefetch_related('comments__user').get(id=pk)
    except Post.DoesNotExist:
        return Response({'status': 'error', 'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({
        'status': 'success',
        'message': 'Post fetched successfully',
        'data': {'post': PostSerializer(post).data},
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    title = request.data.get('title')
    content = request.data.get('content')

    if not title or not content:
        return Response(
            {'status': 'error', 'message': 'Title and Content are required'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    post = Post.objects.create(
        title=title,
        content=content,
        image_url=request.data.get('image_url', ''),
        is_paid=request.data.get('is_paid', False),
        user=request.user,
    )
    return Response({
        'status': 'success',
        'message': 'Post created successfully',
        'data': {'result': PostSerializer(post).data},
    })


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_post(request, pk):
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return Response({'status': 'error', 'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    for field in ['title', 'content', 'image_url', 'is_paid']:
        if field in request.data:
            setattr(post, field, request.data[field])
    post.save()

    return Response({'status': 'success', 'message': 'Post updated successfully'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, pk):
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return Response(
            {'status': 'error', 'message': 'Post not found or already deleted'},
            status=status.HTTP_404_NOT_FOUND,
        )
    post.delete()
    return Response({'status': 'success', 'message': 'Post deleted successfully'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_post(request, post_id):
    try:
        post = Post.objects.select_related('user').get(id=post_id)
    except Post.DoesNotExist:
        return Response({'status': 'error', 'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    from src.serializers.user_serializers import UserSerializer
    return Response({
        'status': 'success',
        'message': 'User found',
        'data': {'user': UserSerializer(post.user).data},
    })


# Comment views

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_comments_by_post(request, post_id):
    comments = Comment.objects.filter(post_id=post_id).select_related('user')
    return Response({
        'status': 'success',
        'message': 'Comments fetched successfully',
        'data': {'comments': CommentSerializer(comments, many=True).data},
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request, post_id):
    content = request.data.get('content')
    if not content:
        return Response({'status': 'error', 'message': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'status': 'error', 'message': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    comment = Comment.objects.create(
        content=content, user=request.user, post=post)
    return Response({
        'status': 'success',
        'message': 'Comment created successfully',
        'data': {'comment': CommentSerializer(comment).data},
    }, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_comment(request, post_id, pk):
    try:
        comment = Comment.objects.select_related('user').get(id=pk)
    except Comment.DoesNotExist:
        return Response({'status': 'error', 'message': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

    if comment.user.id != request.user.id:
        return Response(
            {'status': 'error', 'message': 'You can only update your own comments'},
            status=status.HTTP_403_FORBIDDEN,
        )

    comment.content = request.data.get('content', comment.content)
    comment.save()
    return Response({
        'status': 'success',
        'message': 'Comment updated successfully',
        'data': {'comment': CommentSerializer(comment).data},
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, post_id, pk):
    try:
        comment = Comment.objects.select_related('user').get(id=pk)
    except Comment.DoesNotExist:
        return Response({'status': 'error', 'message': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

    if comment.user.id != request.user.id:
        return Response(
            {'status': 'error', 'message': 'You can only delete your own comments'},
            status=status.HTTP_403_FORBIDDEN,
        )

    comment.delete()
    return Response({'status': 'success', 'message': 'Comment deleted successfully'})
