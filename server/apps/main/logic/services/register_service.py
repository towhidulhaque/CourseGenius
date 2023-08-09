from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from server.apps.main.models import User
from server.apps.main.utils.email_sender import send_email_with_template


class RegisterService(object):
    """User register service."""

    @classmethod
    def register_user(cls, validated_data, active=False, is_verified=False) -> User:
        """New user register method."""
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['username'],
            is_faculty=validated_data.get('is_faculty', False),
            institute=validated_data.get('institute', None),
        )
        user.set_password(validated_data['password'])
        user.is_active = active
        user.is_verified = is_verified
        user.save()
        if not active:
            cls.send_verification_email(user)
        return user

    @classmethod
    def send_verification_email(cls, user):
        """Send email to new registered user."""
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        verification_url = '{base_url}/uidb64/{uidb64}/token/{token}'.format(
            base_url=settings.FRONTEND_BASE_URL,
            uidb64=uid,
            token=token,
        )

        context = {
            'verification_link': verification_url,
        }
        send_email_with_template.delay('register_email', [user.email], context)

    @classmethod
    def verify_email(cls, user: User) -> User:
        """Verify User's email."""
        user.is_email_confirmed = True
        user.activation_code = ''
        user.save()
        return user
