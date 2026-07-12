from django.contrib import admin

from .models import BlacklistedToken, Comment, Follow, Post, Role, Todo, User

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Todo)
admin.site.register(Follow)
admin.site.register(BlacklistedToken)
