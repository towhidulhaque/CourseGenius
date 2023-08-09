# flake8: noqa
import logging
from typing import Dict, List, Optional

from celery import shared_task
from django.core.mail import EmailMessage

from server.apps.main.models.email_template import EmailTemplate

logger = logging.getLogger('django')


@shared_task
def send_email_with_template(
    template_key: str,
    recipient_list: List[str],
    context: Dict[str, str],
    subject: Optional[str] = None,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None,
    attachments: Optional[List[str]] = None,
):
    """
    Send an email using a template retrieved from the EmailTemplate model.

    Args:
        template_key (str): Key to identify the template in the database.
        recipient_list (list): List of recipient email addresses.
        context (dict): Dictionary containing values to replace placeholders in the template.
        subject (str, optional): Email subject. If not provided, it comes from the template.
        cc (list, optional): List of CC email addresses.
        bcc (list, optional): List of BCC email addresses.
        attachments (list, optional): List of file paths to attach.

    """
    try:
        email_template = EmailTemplate.objects.get(template_key=template_key)

        subject = email_template.get_subject(subject, context)
        body = email_template.get_body('', context)  # Body doesn't have an optional argument, using empty string
        from_email = email_template.get_sender()
        recipient_list = email_template.get_recipient(recipient_list, context)

        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=from_email,
            to=recipient_list,
            cc=cc,
            bcc=bcc,
        )

        if attachments:
            for attachment in attachments:
                email.attach_file(attachment)

        email.send()

    except EmailTemplate.DoesNotExist:
        logger.error('Email template not found: {0}'.format(template_key))
