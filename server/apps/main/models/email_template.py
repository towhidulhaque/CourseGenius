from typing import Dict, List

from django import template
from django.db import models
from django.template import Template as DjangoTemplate

from server.apps.utility.base_mixin import BaseMixin
from server.apps.utility.blameable_mixin import BlameableMixin

max_length_medium = 255


class EmailTemplate(BaseMixin, BlameableMixin):
    """Email Template Model."""

    subject = models.CharField(max_length=max_length_medium, blank=True)
    to_email = models.CharField(max_length=max_length_medium, blank=True)
    from_email = models.CharField(max_length=max_length_medium, blank=True)
    mail_body = models.TextField(blank=True)
    is_html = models.BooleanField(default=False)
    template_key = models.CharField(max_length=max_length_medium, unique=True)

    def get_rendered_template(self, tpl: str, context: Dict[str, str]) -> str:
        """Will return parsed content."""
        return self.get_template(tpl).render(context)

    def get_template(self, tpl: str) -> DjangoTemplate:
        """Will return template."""
        return template.Template(tpl)

    def get_subject(  # NOQA: WPS615
        self,
        subject: str,
        context: Dict[str, str],
    ) -> str:
        """Will return email subject."""
        return subject or self.get_rendered_template(self.subject, context)

    def get_body(self, body: str, context: Dict[str, str]) -> str:
        """Email body."""
        return body or self.get_rendered_template(self.mail_body, context)

    def get_sender(self) -> str:
        """Email sender name."""
        return self.from_email

    def get_recipient(
        self,
        emails: List[str],
        context: Dict[str, str],
    ) -> List[str]:
        """All the recipients."""
        return emails or [self.get_rendered_template(self.to_email, context)]
