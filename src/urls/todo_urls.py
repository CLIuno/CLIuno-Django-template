from django.urls import path

from src.views.todo_views import (
    create_todo,
    delete_todo,
    get_all_todos,
    get_current_user_todos,
    get_todo_by_id,
    toggle_todo,
    update_todo,
)

urlpatterns = [
    path('current-user', get_current_user_todos, name='todo-current-user'),
    path('', get_all_todos, name='todo-list'),
    path('create', create_todo, name='todo-create'),
    path('<uuid:pk>', get_todo_by_id, name='todo-detail'),
    path('<uuid:pk>/update', update_todo, name='todo-update'),
    path('<uuid:pk>/delete', delete_todo, name='todo-delete'),
    path('<uuid:pk>/toggle', toggle_todo, name='todo-toggle'),
]
