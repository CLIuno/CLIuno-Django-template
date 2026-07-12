from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def method_dispatch(**views):
    """Route one URL to different DRF function views by HTTP method.

    Each target view is a regular @api_view-decorated function, so it keeps
    its own auth/permission handling; this wrapper only picks which one runs.
    """
    @csrf_exempt
    def view(request, *args, **kwargs):
        handler = views.get(request.method)
        if handler is None:
            return JsonResponse(
                {'status': 'error', 'message': f'Method "{request.method}" not allowed.'},
                status=405,
            )
        return handler(request, *args, **kwargs)

    return view
