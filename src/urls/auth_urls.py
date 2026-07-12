from django.urls import path

from src.views.auth_views import (
    change_password_view,
    check_token_view,
    forgot_password_view,
    login_view,
    logout_view,
    otp_disable_view,
    otp_generate_view,
    otp_validate_view,
    otp_verify_view,
    refresh_token_view,
    register_view,
    reset_password_view,
    send_verify_email_view,
    verify_email_view,
)

urlpatterns = [
    # Authentication
    path('login', login_view, name='auth-login'),
    path('register', register_view, name='auth-register'),
    path('logout', logout_view, name='auth-logout'),
    path('refresh-token', refresh_token_view, name='auth-refresh-token'),
    path('check-token', check_token_view, name='auth-check-token'),
    # Email Verification
    path('send-verify-email', send_verify_email_view,
         name='auth-send-verify-email'),
    path('verify-email', verify_email_view, name='auth-verify-email'),
    # Password Management
    path('forgot-password', forgot_password_view, name='auth-forgot-password'),
    path('reset-password', reset_password_view, name='auth-reset-password'),
    path('change-password', change_password_view, name='auth-change-password'),
    # OTP Management
    path('otp/verify', otp_verify_view, name='auth-otp-verify'),
    path('otp/generate', otp_generate_view, name='auth-otp-generate'),
    path('otp/validate', otp_validate_view, name='auth-otp-validate'),
    path('otp/disable', otp_disable_view, name='auth-otp-disable'),
]
