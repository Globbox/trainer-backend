from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    """Генератор токена сброса пароля."""

    def _make_hash_value(self, user, timestamp):
        return f'{user.pk}{user.is_active}{timestamp}'


class EmailConfirmationTokenGenerator(PasswordResetTokenGenerator):
    """Генератор токена для подтверждения email."""

    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{user.email}{user.is_active}{timestamp}"


password_reset_token = TokenGenerator()
email_confirm_token = EmailConfirmationTokenGenerator()
