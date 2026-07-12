from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.models import Follow, User
from src.serializers.user_serializers import UserSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    if str(request.user.id) == str(user_id):
        return Response({'status': 'error', 'message': 'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        following = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if Follow.objects.filter(follower=request.user, following=following).exists():
        return Response(
            {'status': 'error', 'message': 'Already following this user'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    Follow.objects.create(follower=request.user, following=following)
    return Response({'status': 'success', 'message': 'User followed successfully'}, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    try:
        follow = Follow.objects.get(
            follower=request.user, following_id=user_id)
    except Follow.DoesNotExist:
        return Response({'status': 'error', 'message': 'Not following this user'}, status=status.HTTP_404_NOT_FOUND)

    follow.delete()
    return Response({'status': 'success', 'message': 'User unfollowed successfully'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_followers(request, user_id):
    follows = Follow.objects.filter(
        following_id=user_id).select_related('follower')
    followers = [f.follower for f in follows]
    return Response({
        'status': 'success',
        'message': 'Followers fetched successfully',
        'data': {'followers': UserSerializer(followers, many=True).data},
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_following(request, user_id):
    follows = Follow.objects.filter(
        follower_id=user_id).select_related('following')
    following = [f.following for f in follows]
    return Response({
        'status': 'success',
        'message': 'Following fetched successfully',
        'data': {'following': UserSerializer(following, many=True).data},
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_following(request, user_id):
    is_following = Follow.objects.filter(
        follower=request.user, following_id=user_id).exists()
    return Response({
        'status': 'success',
        'data': {'isFollowing': is_following},
    })
