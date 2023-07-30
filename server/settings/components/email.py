from server.settings.components import config
from server.settings.components.common import INSTALLED_APPS

# EMAIL

DEFAULT_FROM_EMAIL = config(
    'DJANGO_DEFAULT_FROM_EMAIL', default='coursegenius <no-reply@wiseturn.com>',
)
SERVER_EMAIL = config('DJANGO_SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)
EMAIL_SUBJECT_PREFIX = config(
    'DJANGO_EMAIL_SUBJECT_PREFIX', default='[coursegenius-api]',
)

# Anymail
# ------------------------------------------------------------------------------
INSTALLED_APPS += ('anymail',)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = bool(config('EMAIL_USE_TLS') == 'True')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = config('EMAIL_PORT')
