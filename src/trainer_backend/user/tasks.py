from trainer_backend.celery_config import celery_app
from trainer_backend.core.mail_send.confirm_email import ConfirmEmailSender
from trainer_backend.core.mail_send.reset_password import (
    ResetPasswordEmailSender)


@celery_app.task
def reset_password_task(email, reset_url, **kwargs):
    """Задача на отправку письма о сбросе пароля."""
    ResetPasswordEmailSender().send(
        email, reset_url
    )


@celery_app.task
def confirm_email_task(email, reset_url, **kwargs):
    """Задача на отправку письма о подтверждении email."""
    ConfirmEmailSender().send(
        email, reset_url
    )
