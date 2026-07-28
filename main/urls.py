from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve

from src.helpers.upload import ensure_upload_dir

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'api/{settings.API_VERSION}/', include('src.urls')),
    # Uploaded images are public and unversioned — no /api/v1 prefix, no auth.
    re_path(
        r'^uploads/(?P<path>[\w.-]+)$',
        serve,
        {'document_root': str(ensure_upload_dir())},
        name='upload-serve',
    ),
]
