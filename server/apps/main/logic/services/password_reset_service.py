from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from server.apps.main.utils.email_sender import send_email_with_template


class PasswordResetService(object):
    """Service for password reset."""

    @classmethod
    def handle_password_reset_request(cls, user):
        """Handle password request request."""
        uidb64, token = cls.generate_reset_token(user)
        cls.send_reset_email(user, uidb64, token)

    @classmethod
    def generate_reset_token(cls, user):
        """
        Generate a reset token for the given user.

        Args:
            user (User): The user for whom the reset token is generated.

        Returns:
            tuple: A tuple containing uidb64 and token.
        """
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        return uidb64, token

    @classmethod
    def send_reset_email(cls, user, uidb64, token):
        """
        Send a password reset email to the user with the reset link.

        Args:
            user (User): The user who requested the password reset.
            uidb64 (str): Base64-encoded user ID.
            token (str): Password reset token.
        """
        reset_link = '{base_url}/password-reset/uidb64/{uidb64}/token/{token}'.format(
            base_url=settings.FRONTEND_BASE_URL,
            uidb64=uidb64,
            token=token,
        )

        context = {
            'reset_link': reset_link,
            'name': user.first_name,
        }
        send_email_with_template.delay('password_reset_email', [user.email], context)

    @classmethod
    def reset_password(cls, user, new_password):
        """
        Reset the user's password.

        Args:
            user (User): The user whose password needs to be reset.
            new_password (str): The new password for the user.
        """
        user.set_password(new_password)
        user.save()
