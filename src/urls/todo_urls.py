from django.urls import path

from src.urls.dispatch import method_dispatch
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
    path('/current-user', get_current_user_todos, name='todo-current-user'),
    path('', method_dispatch(GET=get_all_todos, POST=create_todo), name='todo-collection'),
    path('/<uuid:pk>',
         method_dispatch(GET=get_todo_by_id, PATCH=update_todo, DELETE=delete_todo),
         name='todo-detail'),
    path('/<uuid:pk>/toggle', toggle_todo, name='todo-toggle'),
]
