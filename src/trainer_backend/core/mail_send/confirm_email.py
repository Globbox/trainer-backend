from .base import BaseEmailSender


class ConfirmEmailSender(BaseEmailSender):
    """Класс для отправки писем о подтверждении email."""

    subject = "Подтверждение email"
    template_name = "email/confirm_email.html"

    def send(self, email, confirm_email_url, *args, **kwargs):
        """Отправить письмо о подтверждении email."""
        super().send([email], *args, context={
            'confirm_email_url': confirm_email_url
        }, **kwargs)
