from abc import ABC
from datetime import date

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class AbstractEmailSender(ABC):
    """Абстрактный класс для отправки писем."""

    template_name = None
    from_email = None
    subject = None
    context = None

    def __init__(self):
        if self.template_name is None:
            raise ValueError('template_name must be set')

        if self.from_email is None:
            raise ValueError('from_email must be set')

        self.context = self.context or {}

    def send(self, to_emails, *args, subject=None, context=None, **kwargs):
        """Отправить письмо."""
        html_content = render_to_string(
            self.template_name, {**self.context, **(context or {})}
        )

        email = EmailMessage(
            subject=subject or self.subject,
            body=html_content,
            from_email=self.from_email,
            to=to_emails,
        )
        email.content_subtype = 'html'
        email.send()


class BaseEmailSender(AbstractEmailSender, ABC):
    """Базовый класс для отправки писем."""

    from_email = settings.DEFAULT_FROM_EMAIL

    def __init__(self):
        super(BaseEmailSender, self).__init__()
        self.context = {
            'year': date.today().year
        }
