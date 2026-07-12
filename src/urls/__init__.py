from django.urls import include, path

urlpatterns = [
    path('auth/', include('src.urls.auth_urls')),
    path('users', include('src.urls.user_urls')),
    path('roles/', include('src.urls.role_urls')),
    path('posts', include('src.urls.post_urls')),
    path('todos', include('src.urls.todo_urls')),
    path('follows', include('src.urls.follow_urls')),
]
