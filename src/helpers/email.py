import secrets

from django.conf import settings
from django.core.mail import send_mail


def generate_token():
    return secrets.token_urlsafe(32)


def send_verify_email(email, token, user_id):
    frontend_url = settings.FRONTEND_URL
    html = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.6;">
        <h2>Hello,</h2>
        <p>Thank you for registering. Click the button below to verify your email address:</p>
        <a href="{frontend_url}/auth/verify-email?token={token}&userId={user_id}"
           style="display: inline-block; padding: 10px 20px; font-size: 16px; color: #fff;
                  background-color: #28a745; text-decoration: none; border-radius: 5px;">
          Verify Email
        </a>
        <p>If you did not register for an account, please ignore this email.</p>
        <p>Thank you,<br>Your Company Team</p>
    </div>
    """
    send_mail(
        subject='Verify your email address',
        message='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        html_message=html,
        fail_silently=True,
    )


def send_reset_password_email(email, token, user_id):
    frontend_url = settings.FRONTEND_URL
    html = f"""
    <div style="font-family: Arial, sans-serif; line-height: 1.6;">
        <h2>Hello,</h2>
        <p>You requested to reset your password. Click the button below to reset it:</p>
        <a href="{frontend_url}/auth/reset-password?token={token}&userId={user_id}"
           style="display: inline-block; padding: 10px 20px; font-size: 16px; color: #fff;
                  background-color: #007bff; text-decoration: none; border-radius: 5px;">
          Reset Password
        </a>
        <p>If you did not request a password reset, please ignore this email.</p>
        <p>Thank you,<br>Your Company Team</p>
    </div>
    """
    send_mail(
        subject='Reset your password',
        message='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        html_message=html,
        fail_silently=True,
    )
