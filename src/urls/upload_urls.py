from django.urls import path

from src.views.upload_views import upload_image

urlpatterns = [
    path('/image', upload_image, name='upload-image'),
]
