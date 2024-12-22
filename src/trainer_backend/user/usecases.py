import posixpath

from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from trainer_backend.core.common.usecase import AbstractUseCase
from trainer_backend.user.generators import email_confirm_token
from trainer_backend.user.generators import password_reset_token

from .models import User
from .tasks import confirm_email_task
from .tasks import reset_password_task


class ResetUserPasswordUseCase(AbstractUseCase):
    """UseCase для сброса пароля пользователя."""

    def execute(self, user, *args, **kwargs):
        """Сбросить пароль на пользователе."""
        if not isinstance(user, User):
            raise ValueError("Incorrect user")

        token = password_reset_token.make_token(user)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = posixpath.join(
            settings.PASSWORD_RESET_URL, f'{uid}/{token}'
        )

        reset_password_task.delay(
            user.email, reset_url
        )


class ConfirmEmailUseCase(AbstractUseCase):
    """UseCase для подтверждения email пользователя."""

    def execute(self, user, *args, **kwargs):
        """Подтвердить email пользователя."""
        if not isinstance(user, User):
            raise ValueError("Incorrect user")

        token = email_confirm_token.make_token(user)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = posixpath.join(
            settings.CONFIRM_EMAIL_URL, f'{uid}/{token}'
        )

        confirm_email_task.delay(
            user.email, reset_url
        )
