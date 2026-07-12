from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.models import Todo, User
from src.serializers.todo_serializers import TodoSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user_todos(request):
    todos = Todo.objects.filter(user=request.user)
    return Response({
        'status': 'success',
        'message': 'Todos fetched successfully',
        'data': {'todos': TodoSerializer(todos, many=True).data},
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_todos(request):
    todos = Todo.objects.select_related('user').all()
    return Response({
        'status': 'success',
        'message': 'Todos fetched successfully',
        'data': {'todos': TodoSerializer(todos, many=True).data},
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_todo_by_id(request, pk):
    try:
        todo = Todo.objects.select_related('user').get(id=pk)
    except Todo.DoesNotExist:
        return Response({'status': 'error', 'message': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({
        'status': 'success',
        'message': 'Todo fetched successfully',
        'data': {'todo': TodoSerializer(todo).data},
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_todo(request):
    title = request.data.get('title')
    if not title:
        return Response({'status': 'error', 'message': 'Title is required'}, status=status.HTTP_400_BAD_REQUEST)

    todo = Todo.objects.create(
        title=title,
        description=request.data.get('description', ''),
        user=request.user,
    )
    return Response({
        'status': 'success',
        'message': 'Todo created successfully',
        'data': {'todo': TodoSerializer(todo).data},
    }, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_todo(request, pk):
    try:
        todo = Todo.objects.select_related('user').get(id=pk)
    except Todo.DoesNotExist:
        return Response({'status': 'error', 'message': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND)

    if todo.user.id != request.user.id:
        return Response(
            {'status': 'error', 'message': 'You can only update your own todos'},
            status=status.HTTP_403_FORBIDDEN,
        )

    for field in ['title', 'description', 'is_completed']:
        if field in request.data:
            setattr(todo, field, request.data[field])
    todo.save()

    return Response({
        'status': 'success',
        'message': 'Todo updated successfully',
        'data': {'todo': TodoSerializer(todo).data},
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_todo(request, pk):
    try:
        todo = Todo.objects.select_related('user').get(id=pk)
    except Todo.DoesNotExist:
        return Response({'status': 'error', 'message': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND)

    if todo.user.id != request.user.id:
        return Response(
            {'status': 'error', 'message': 'You can only delete your own todos'},
            status=status.HTTP_403_FORBIDDEN,
        )

    todo.delete()
    return Response({'status': 'success', 'message': 'Todo deleted successfully'})


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def toggle_todo(request, pk):
    try:
        todo = Todo.objects.select_related('user').get(id=pk)
    except Todo.DoesNotExist:
        return Response({'status': 'error', 'message': 'Todo not found'}, status=status.HTTP_404_NOT_FOUND)

    if todo.user.id != request.user.id:
        return Response(
            {'status': 'error', 'message': 'You can only update your own todos'},
            status=status.HTTP_403_FORBIDDEN,
        )

    todo.is_completed = not todo.is_completed
    todo.save()
    return Response({
        'status': 'success',
        'message': 'Todo toggled successfully',
        'data': {'todo': TodoSerializer(todo).data},
    })
