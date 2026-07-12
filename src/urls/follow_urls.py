from django.urls import path

from src.views.follow_views import (
    follow_user,
    get_followers,
    get_following,
    is_following,
    unfollow_user,
)

urlpatterns = [
    path('<uuid:user_id>/follow', follow_user, name='follow-user'),
    path('<uuid:user_id>/unfollow', unfollow_user, name='unfollow-user'),
    path('<uuid:user_id>/followers', get_followers, name='followers'),
    path('<uuid:user_id>/following', get_following, name='following'),
    path('<uuid:user_id>/is-following', is_following, name='is-following'),
]
