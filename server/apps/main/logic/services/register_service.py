from server.apps.main.models import User


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
            # todo: send OTP
            pass  # noqa: WPS420
        return user
