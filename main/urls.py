from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'api/{settings.API_VERSION}/', include('src.urls')),
]
