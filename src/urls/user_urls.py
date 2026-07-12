from django.urls import path

from src.views.user_views import (
    current_user_view,
    delete_user_by_id,
    get_all_users,
    get_posts_by_user,
    get_roles_by_user,
    get_user_by_id,
    get_user_by_username,
    update_user_by_id,
)

urlpatterns = [
    path('current', current_user_view, name='user-current'),
    path('username/<str:username>', get_user_by_username, name='user-by-username'),
    path('posts', get_posts_by_user, name='user-posts'),
    path('role', get_roles_by_user, name='user-role'),
    path('<uuid:pk>', get_user_by_id, name='user-by-id'),
    # Admin routes
    path('', get_all_users, name='user-list'),
    path('<uuid:pk>/update', update_user_by_id, name='user-update'),
    path('<uuid:pk>/delete', delete_user_by_id, name='user-delete'),
]
