from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


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

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    """Модель пользователя."""

    date_joined = models.DateTimeField(
        default=timezone.now
    )
    is_student = models.BooleanField(
        default=False
    )
    is_teacher = models.BooleanField(
        default=False
    )
    email = models.EmailField(
        verbose_name='Email',
        unique=True
    )
    fio = models.CharField(
        max_length=255
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fio']
