from django.urls import path

from src.urls.dispatch import method_dispatch
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
    path('/current', current_user_view, name='user-current'),
    path('/username/<str:username>', get_user_by_username, name='user-by-username'),
    path('', get_all_users, name='user-list'),
    path('/<uuid:pk>',
         method_dispatch(GET=get_user_by_id, PATCH=update_user_by_id, DELETE=delete_user_by_id),
         name='user-detail'),
    path('/<uuid:pk>/posts', get_posts_by_user, name='user-posts'),
    path('/<uuid:pk>/roles', get_roles_by_user, name='user-roles'),
]
