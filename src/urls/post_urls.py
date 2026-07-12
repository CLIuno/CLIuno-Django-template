from django.urls import path

from src.urls.dispatch import method_dispatch
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
    path('/current-user', get_current_user_posts, name='post-current-user'),
    path('', method_dispatch(GET=get_all_posts, POST=create_post), name='post-collection'),
    path('/<uuid:pk>',
         method_dispatch(GET=get_post_by_id, PATCH=update_post, DELETE=delete_post),
         name='post-detail'),
    path('/<uuid:post_id>/user', get_user_by_post, name='post-user'),
    # Comments
    path('/<uuid:post_id>/comments',
         method_dispatch(GET=get_comments_by_post, POST=create_comment),
         name='post-comments'),
    path('/<uuid:post_id>/comments/<uuid:pk>',
         method_dispatch(PATCH=update_comment, DELETE=delete_comment),
         name='post-comment-detail'),
]
