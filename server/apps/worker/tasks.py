# flake8: noqa WPS211
import logging

from server.celery import app as celery_app

log = logging.getLogger(__name__)

__all__ = ['celery_app']  # noqa: WPS410
MAX_RETRIES = 2
