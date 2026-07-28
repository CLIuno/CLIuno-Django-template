from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.helpers.upload import (
    ALLOWED_IMAGE_TYPES,
    MAX_UPLOAD_BYTES,
    ensure_upload_dir,
    generated_filename,
    public_upload_url,
)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_image(request):
    """Store the bytes and hand back a URL.

    Attaching it to a user or a post is the caller's job
    (PATCH /users/current, POST /posts) — upload mutates nothing.
    """
    uploaded = request.FILES.get('file')
    if not uploaded:
        return Response(
            {'status': 'warning', 'message': 'No image file provided'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if uploaded.content_type not in ALLOWED_IMAGE_TYPES:
        return Response(
            {'status': 'error', 'message': f'Unsupported image type: {uploaded.content_type}'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if uploaded.size > MAX_UPLOAD_BYTES:
        return Response(
            {'status': 'error', 'message': 'Image exceeds the 5 MB limit'},
            status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        )

    filename = generated_filename(uploaded.content_type)
    target = ensure_upload_dir() / filename
    with open(target, 'wb') as destination:
        destination.writelines(uploaded.chunks())

    return Response(
        {
            'status': 'success',
            'message': 'Image uploaded',
            'data': {'url': public_upload_url(request, filename), 'filename': filename},
        },
        status=status.HTTP_201_CREATED,
    )
