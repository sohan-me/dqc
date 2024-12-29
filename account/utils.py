from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

# To get refresh token for a user
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def send_activation_email(user, request):
    """
    Generate an activation URL and send an activation email to the user.
    """
    current_site = get_current_site(request)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_link = f"http://{current_site.domain}/api/activate/{uid}/{token}/"

    email_subject = "DQC | Activate your account"
    email_body = f"""
    Hi {user.first_name},

    Thank you for registering. Please use the link below to activate your account:

    {activation_link}

    If you didn't register, you can safely ignore this email.
    """
    send_mail(
        email_subject,
        email_body,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False
    )


def send_password_reset_email(user, request):
    """
    Generate an Password Reset URL and send an password reset email to the user.
    """
    current_site = get_current_site(request)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    reset_link = f"http://{current_site.domain}/api/reset_password/{uid}/{token}/"

    email_subject = "DQC | Reset your Password"
    email_body = f"""
    Hi {user.first_name},

    Did you try to reset your password! Please use the link below to reset your password:

    {reset_link}

    If you didn't made this attempt, please make a security check.
    """
    send_mail(
        email_subject,
        email_body,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False
    )