import pyotp
from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from src.helpers.email import (
    generate_token,
    send_reset_password_email,
    send_verify_email,
)
from src.models import BlacklistedToken, Role, User
from src.serializers.user_serializers import (
    ChangePasswordSerializer,
    LoginSerializer,
    RegisterSerializer,
    ResetPasswordSerializer,
)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'status': 'warning', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    username_or_email = serializer.validated_data['usernameOrEmail']
    password = serializer.validated_data['password']

    # Try to find user by email or username
    try:
        if '@' in username_or_email:
            user = User.objects.get(email=username_or_email)
        else:
            user = User.objects.get(username=username_or_email)
    except User.DoesNotExist:
        return Response(
            {'status': 'error', 'message': 'Invalid username/email or password'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if user.is_deleted:
        return Response({'status': 'error', 'message': 'User is deleted'}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.is_verified:
        return Response(
            {'status': 'warning', 'message': 'Please verify your email address'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if not user.check_password(password):
        return Response(
            {'status': 'error', 'message': 'Wrong username/email or password'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    refresh = RefreshToken.for_user(user)

    return Response({
        'status': 'success',
        'message': 'Login successful',
        'data': {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_otp_enabled': user.is_otp_enabled,
            'token': str(refresh.access_token),
            'refreshToken': str(refresh),
        },
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'status': 'warning', 'message': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    data = serializer.validated_data

    if User.objects.filter(Q(username=data['username']) | Q(email=data['email'])).exists():
        return Response(
            {'status': 'warning', 'message': 'User already exists'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    role, _ = Role.objects.get_or_create(name='user')

    user = User.objects.create_user(
        email=data['email'],
        username=data['username'],
        password=data['password'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        role=role,
    )

    token = generate_token()
    send_verify_email(user.email, token, str(user.id))

    return Response(
        {
            'status': 'success',
            'message': 'User created successfully and an email has been sent to you for verification',
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return Response({'status': 'warning', 'message': 'No token provided'}, status=status.HTTP_400_BAD_REQUEST)

    if BlacklistedToken.objects.filter(token=token).exists():
        return Response(
            {'status': 'warning', 'message': 'Token has already been invalidated'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    BlacklistedToken.objects.create(token=token)
    return Response({'status': 'success', 'message': 'Logout successful'})


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token_view(request):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return Response({'status': 'warning', 'message': 'No token provided'}, status=status.HTTP_400_BAD_REQUEST)

    if BlacklistedToken.objects.filter(token=token).exists():
        return Response(
            {'status': 'warning', 'message': 'Token has already been invalidated'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    try:
        old_refresh = RefreshToken(token)
        user = User.objects.get(id=old_refresh['user_id'])
        new_refresh = RefreshToken.for_user(user)

        # Blacklist the old token
        BlacklistedToken.objects.create(token=token)

        return Response({
            'status': 'success',
            'message': 'Token refreshed successfully',
            'data': {
                'token': str(new_refresh.access_token),
                'refreshToken': str(new_refresh),
            },
        })
    except Exception:
        return Response({'status': 'error', 'message': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_token_view(request):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')

    if BlacklistedToken.objects.filter(token=token).exists():
        return Response(
            {'status': 'warning', 'message': 'Token has already been invalidated'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    return Response({'status': 'success', 'message': 'Token is valid'})


@api_view(['POST'])
@permission_classes([AllowAny])
def send_verify_email_view(request):
    # Authenticated requests derive the target user; `email` is a fallback.
    if getattr(request, 'user', None) and request.user.is_authenticated:
        user = request.user
    else:
        email = request.data.get('email')
        if not email:
            return Response({'status': 'warning', 'message': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    token = generate_token()
    send_verify_email(user.email, token, str(user.id))

    return Response({'status': 'success', 'message': 'Email sent successfully'})


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_email_view(request):
    user_id = request.data.get('user_id')
    token = request.data.get('token')

    if not user_id or not token:
        return Response(
            {'status': 'warning', 'message': 'user_id and token are required'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'status': 'error', 'message': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    if BlacklistedToken.objects.filter(token=token).exists():
        return Response(
            {'status': 'warning', 'message': 'Token has already been invalidated'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    BlacklistedToken.objects.create(token=token)
    user.is_verified = True
    user.save()

    refresh = RefreshToken.for_user(user)

    return Response({
        'status': 'success',
        'message': 'Email verified successfully',
        'data': {
            'token': str(refresh.access_token),
            'refreshToken': str(refresh),
        },
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password_view(request):
    # Frontends send `email`; `usernameOrEmail` is kept for compatibility
    username_or_email = request.data.get('email') or request.data.get('usernameOrEmail')
    if not username_or_email:
        return Response(
            {'status': 'warning', 'message': 'Email is required'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        if '@' in username_or_email:
            user = User.objects.get(email=username_or_email)
        else:
            user = User.objects.get(username=username_or_email)
    except User.DoesNotExist:
        return Response(
            {'status': 'error', 'message': 'Invalid username/email or password'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token = generate_token()
    send_reset_password_email(user.email, token, str(user.id))

    return Response({'status': 'success', 'message': 'Email sent successfully'})


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_view(request):
    serializer = ResetPasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'status': 'warning', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data

    try:
        user = User.objects.get(id=data['user_id'])
    except User.DoesNotExist:
        return Response({'status': 'error', 'message': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

    if BlacklistedToken.objects.filter(token=data['token']).exists():
        return Response(
            {'status': 'warning', 'message': 'Token has already been invalidated'},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    BlacklistedToken.objects.create(token=data['token'])
    user.set_password(data['password'])
    user.save()

    return Response({'status': 'success', 'message': 'Password reset successful'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    serializer = ChangePasswordSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({'status': 'warning', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    request.user.set_password(serializer.validated_data['password'])
    request.user.save()

    return Response({'status': 'success', 'message': 'Password changed successfully'})


# OTP Views

def _resolve_request_user(request):
    """Authenticated requests act on the current user; usernameOrEmail is a fallback."""
    if getattr(request, 'user', None) and request.user.is_authenticated:
        return request.user

    username_or_email = request.data.get('usernameOrEmail')
    if not username_or_email:
        return None
    try:
        if '@' in username_or_email:
            return User.objects.get(email=username_or_email)
        return User.objects.get(username=username_or_email)
    except User.DoesNotExist:
        return None


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def otp_generate_view(request):
    user = _resolve_request_user(request)
    if user is None:
        return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    provisioning_uri = totp.provisioning_uri(
        name=user.username, issuer_name=request.build_absolute_uri('/'))

    user.otp_base32 = secret
    user.otp_auth_url = provisioning_uri
    user.save()

    return Response({
        'status': 'success',
        'message': 'OTP secret generated',
        'data': {
            'secret': secret,
            'base32': secret,
            'otpauth_url': provisioning_uri,
        },
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def otp_verify_view(request):
    user = _resolve_request_user(request)
    token = request.data.get('otp') or request.data.get('token')

    if user is None:
        return Response(
            {'status': 'error', 'message': 'Token is invalid or user does not exist'},
            status=status.HTTP_404_NOT_FOUND,
        )

    if not user.otp_base32:
        return Response({'status': 'error', 'message': 'OTP not set up'}, status=status.HTTP_400_BAD_REQUEST)

    totp = pyotp.TOTP(user.otp_base32)
    if not token or not totp.verify(token, valid_window=1):
        return Response({'status': 'error', 'message': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)

    user.is_otp_verified = True
    user.is_otp_enabled = True
    user.save()

    return Response({'status': 'success', 'message': 'OTP verified successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def otp_validate_view(request):
    user = _resolve_request_user(request)
    token = request.data.get('otp') or request.data.get('token')

    if user is None:
        return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if not user.is_otp_enabled:
        return Response(
            {'status': 'error', 'message': 'OTP is not enabled for this user'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    totp = pyotp.TOTP(user.otp_base32)
    if not token or not totp.verify(token, valid_window=1):
        return Response({'status': 'error', 'message': 'Authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)

    return Response({'status': 'success', 'message': 'OTP validated successfully'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def otp_disable_view(request):
    user = _resolve_request_user(request)
    if user is None:
        return Response({'status': 'error', 'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    user.is_otp_enabled = False
    user.otp_base32 = None
    user.otp_auth_url = None
    user.save()

    return Response({'status': 'success', 'message': 'OTP disabled successfully'})
