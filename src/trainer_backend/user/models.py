from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import EmailValidator
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """Менеджер для работы с пользователями."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Создание пользователя и сохранение его в базе данных."""
        if not email:
            raise ValueError("Поле Email является обязательным")
        email = self.normalize_email(email)

        # Непосредственно создание пользователя в БД
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Создание обычного пользователя и сохранение его в базе данных."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Создание админ пользователя и сохранение его в базе данных."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя."""

    objects = UserManager()
    email_validator = EmailValidator()

    email = models.EmailField(
        unique=True,
        error_messages={
            "unique": "Пользователь с таким Email уже существует"
        },
        validators=[email_validator],
        verbose_name="Email",
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата создания",
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name="Superuser",
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name="Администратор",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активный пользователь",
    )

    # Дополнительная информация о пользователе
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Имя",
    )
    second_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Фамилия",
    )
    birthdate = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата рождения",
    )
    phone = models.CharField(
        max_length=11,
        blank=True,
        verbose_name="Телефон",
    )

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    def clean(self):
        """Обработка перед изменением/добавлением."""
        self.email = UserManager.normalize_email(self.email)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
