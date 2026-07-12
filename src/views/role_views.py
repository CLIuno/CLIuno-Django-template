from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from src.models import Role, User
from src.permissions import IsAdmin
from src.serializers.role_serializers import RoleSerializer
from src.serializers.user_serializers import UserSerializer


@api_view(['GET'])
@permission_classes([IsAdmin])
def get_all_roles(request):
    roles = Role.objects.all()
    return Response({
        'status': 'success',
        'message': 'Roles fetched successfully',
        'data': {'roles': RoleSerializer(roles, many=True).data},
    })


@api_view(['GET'])
@permission_classes([IsAdmin])
def get_role_by_id(request, pk):
    try:
        role = Role.objects.get(id=pk)
    except Role.DoesNotExist:
        return Response({'status': 'warning', 'message': 'Role not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({
        'status': 'success',
        'message': 'Role fetched successfully',
        'data': {'role': RoleSerializer(role).data},
    })


@api_view(['POST'])
@permission_classes([IsAdmin])
def create_role(request):
    name = request.data.get('name')
    if not name:
        return Response({'status': 'warning', 'message': 'Role name is required'}, status=status.HTTP_400_BAD_REQUEST)

    if Role.objects.filter(name=name).exists():
        return Response({'status': 'warning', 'message': 'Role already exists'}, status=status.HTTP_400_BAD_REQUEST)

    role = Role.objects.create(name=name)
    return Response({
        'status': 'success',
        'message': 'Role created successfully',
        'data': {'savedRole': RoleSerializer(role).data},
    }, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsAdmin])
def update_role(request, pk):
    try:
        role = Role.objects.get(id=pk)
    except Role.DoesNotExist:
        return Response({'status': 'warning', 'message': 'Role not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = RoleSerializer(role, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response({'status': 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    return Response({
        'status': 'success',
        'message': 'Role updated successfully',
        'data': {'updatedRole': RoleSerializer(role).data},
    })


@api_view(['DELETE'])
@permission_classes([IsAdmin])
def delete_role(request, pk):
    try:
        role = Role.objects.get(id=pk)
    except Role.DoesNotExist:
        return Response({'status': 'warning', 'message': 'Role not found'}, status=status.HTTP_404_NOT_FOUND)

    role.delete()
    return Response({'status': 'success', 'message': 'Role deleted successfully'})


@api_view(['GET'])
@permission_classes([IsAdmin])
def get_users_by_role(request, role_id):
    try:
        role = Role.objects.get(id=role_id)
    except Role.DoesNotExist:
        return Response({'status': 'warning', 'message': 'Role not found'}, status=status.HTTP_404_NOT_FOUND)

    users = User.objects.filter(role=role)
    return Response({
        'status': 'success',
        'message': 'Users found',
        'data': {'users': UserSerializer(users, many=True).data},
    })
