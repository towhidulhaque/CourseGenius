from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, status


class InvalidToken(exceptions.AuthenticationFailed):
    """Will return invalid return error."""

    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Token is invalid or expired')
    default_code = 'token_not_valid'


class TokenNotExist(exceptions.AuthenticationFailed):
    """Will return invalid return error."""

    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Token is not provided.')
    default_code = 'token_not_valid'


class UserNotFound(exceptions.AuthenticationFailed):
    """Will return invalid return error."""

    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('User not found.')


class CompanyNotFound(exceptions.AuthenticationFailed):
    """Will return invalid return error."""

    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('Company not found.')
