import uuid
from pathlib import Path

from django.conf import settings

# Uploaded files live at the repo root and are served back from /uploads.
UPLOAD_DIR = Path(settings.BASE_DIR) / 'uploads'

# 5 MB — matches every other CLIuno backend template.
MAX_UPLOAD_BYTES = 5 * 1024 * 1024

# The extension comes from the detected mime, never from the client's filename.
ALLOWED_IMAGE_TYPES = {
    'image/png': '.png',
    'image/jpeg': '.jpg',
    'image/webp': '.webp',
    'image/gif': '.gif',
}


def ensure_upload_dir():
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    return UPLOAD_DIR


def generated_filename(content_type):
    return f'{uuid.uuid4()}{ALLOWED_IMAGE_TYPES[content_type]}'


def public_upload_url(request, filename):
    """Absolute so a frontend on another origin can use it straight as an image source."""
    base = getattr(settings, 'PUBLIC_BASE_URL', '') or request.build_absolute_uri('/')
    return f'{base.rstrip("/")}/uploads/{filename}'
