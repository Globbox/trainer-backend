from urllib.parse import urljoin

from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from trainer_backend.core.common.usecase import AbstractUseCase
from trainer_backend.core.email.reset_password import ResetPasswordEmailSender
from trainer_backend.user.generators import account_activation_token

from .models import User


class ResetUserPasswordUseCase(AbstractUseCase):
    """UseCase для сброса пароля пользователя."""

    def execute(self, user, *args, **kwargs):
        """Сбросить пароль на пользователе."""
        if not isinstance(user, User):
            raise ValueError("Incorrect user")

        token = account_activation_token.make_token(user)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = urljoin(settings.PASSWORD_RESET_URL, f'{uid}/{token}')

        ResetPasswordEmailSender().send(
            user.email, reset_url
        )
