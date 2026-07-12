from django.urls import path

from src.views.role_views import (
    create_role,
    delete_role,
    get_all_roles,
    get_role_by_id,
    get_users_by_role,
    update_role,
)

urlpatterns = [
    path('', get_all_roles, name='role-list'),
    path('<uuid:pk>', get_role_by_id, name='role-detail'),
    path('create', create_role, name='role-create'),
    path('<uuid:pk>/update', update_role, name='role-update'),
    path('<uuid:pk>/delete', delete_role, name='role-delete'),
    path('<uuid:role_id>/users', get_users_by_role, name='role-users'),
]
