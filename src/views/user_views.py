from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.models import Post, User
from src.permissions import IsAdmin
from src.serializers.user_serializers import UserSerializer, UserUpdateSerializer


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def current_user_view(request):
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response({'status': 'success', 'data': {'user': serializer.data}})

    if request.method == 'PATCH':
        serializer = UserUpdateSerializer(
            request.user, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({'status': 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            'status': 'success',
            'message': 'User updated',
            'data': {'user': UserSerializer(request.user).data},
        })

    if request.method == 'DELETE':
        user = request.user
        user.is_deleted = True
        user.deleted_at = timezone.now()
        user.save()
        return Response({
            'status': 'success',
            'message': 'User deleted',
            'data': {'user': UserSerializer(user).data},
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_username(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'status': 'warning', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'status': 'success', 'data': {'user': UserSerializer(user).data}})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_id(request, pk):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response({'status': 'warning', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'status': 'success', 'data': {'user': UserSerializer(user).data}})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_posts_by_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(
            {'status': 'warning', 'message': 'User not found'},
            status=status.HTTP_404_NOT_FOUND,
        )
    posts = Post.objects.filter(user=user)
    from src.serializers.post_serializers import PostSerializer
    return Response({
        'status': 'success',
        'message': 'User posts fetched successfully',
        'data': {'posts': PostSerializer(posts, many=True).data},
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_roles_by_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(
            {'status': 'warning', 'message': 'User not found'},
            status=status.HTTP_404_NOT_FOUND,
        )
    from src.serializers.role_serializers import RoleSerializer
    if user.role:
        return Response({
            'status': 'success',
            'data': {'role': RoleSerializer(user.role).data},
        })
    return Response({'status': 'success', 'data': {'role': None}})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response({'status': 'success', 'data': {'users': serializer.data}})


# Admin routes


@api_view(['PATCH'])
@permission_classes([IsAdmin])
def update_user_by_id(request, pk):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response({'status': 'warning', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserUpdateSerializer(user, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response({'status': 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    return Response({'status': 'success', 'data': UserSerializer(user).data})


@api_view(['DELETE'])
@permission_classes([IsAdmin])
def delete_user_by_id(request, pk):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response({'status': 'warning', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    user.is_deleted = True
    user.deleted_at = timezone.now()
    user.save()
    return Response({'status': 'success', 'message': 'User deleted', 'data': UserSerializer(user).data})
