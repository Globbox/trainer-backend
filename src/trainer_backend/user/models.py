from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):
    """Менеджер для работы с пользователями."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email - обязательное поле')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff_user(self, email, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        return self.create_user(email, password, **kwargs)

    def create_superuser(self, email, password=None, **kwargs):
        kwargs.setdefault('is_superuser', True)
        return self.create_staff_user(email, password, **kwargs)


class User(PermissionsMixin, AbstractBaseUser):
    """Модель пользователя."""

    objects = UserManager()

    USERNAME_FIELD = 'email'

    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата создания',
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name='Преподаватель',
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name='Администратор',
    )
    email = models.EmailField(
        verbose_name='Email',
        unique=True,
    )

    # Дополнительная информация о пользователе
    first_name = models.CharField(
        max_length=128,
        null=True,
        verbose_name='Имя',
    )
    second_name = models.CharField(
        max_length=128,
        null=True,
        verbose_name='Фамилия',
    )
    birthdate = models.DateField(
        null=True,
        verbose_name='Дата рождения',
    )
    phone = models.CharField(
        max_length=10,
        null=True,
        verbose_name='Телефон',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
