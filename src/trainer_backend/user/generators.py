from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):
    """Генератор токена сброса пароля."""

    def _make_hash_value(self, user, timestamp):
        return f'{user.pk}{user.is_active}{timestamp}'


account_activation_token = TokenGenerator()
