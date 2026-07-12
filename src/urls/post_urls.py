from django.urls import path

from src.views.post_views import (
    create_comment,
    create_post,
    delete_comment,
    delete_post,
    get_all_posts,
    get_comments_by_post,
    get_current_user_posts,
    get_post_by_id,
    get_user_by_post,
    update_comment,
    update_post,
)

urlpatterns = [
    path('current-user', get_current_user_posts, name='post-current-user'),
    path('', get_all_posts, name='post-list'),
    path('create', create_post, name='post-create'),
    path('<uuid:pk>', get_post_by_id, name='post-detail'),
    path('<uuid:pk>/update', update_post, name='post-update'),
    path('<uuid:pk>/delete', delete_post, name='post-delete'),
    path('<uuid:post_id>/user', get_user_by_post, name='post-user'),
    # Comments
    path('<uuid:post_id>/comments', get_comments_by_post, name='comment-list'),
    path('<uuid:post_id>/comments/create',
         create_comment, name='comment-create'),
    path('<uuid:post_id>/comments/<uuid:pk>/update',
         update_comment, name='comment-update'),
    path('<uuid:post_id>/comments/<uuid:pk>/delete',
         delete_comment, name='comment-delete'),
]
