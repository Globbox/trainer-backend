from .base import BaseEmailSender


class ResetPasswordEmailSender(BaseEmailSender):
    """Класс для отправки писем о сбросе пароля."""

    subject = "Сброс пароля"
    template_name = "email/password_reset.html"

    def send(self, email, confirm_reset_password_url, *args, **kwargs):
        """Отправить письмо о сбросе пароля."""
        super().send([email], *args, context={
            'confirm_reset_password_url': confirm_reset_password_url
        }, **kwargs)
