from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from .usecases import ResetUserPasswordUseCase


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Админ панель для редактирования пользователей."""

    list_display = (
        'email', 'first_name', 'second_name', 'is_staff', 'is_superuser'
    )
    search_fields = ('email', 'first_name', 'second_name')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ("Персональная информация",
         {'fields': ('first_name', 'second_name', 'birthdate', 'phone')}),
        ('Доступы', {'fields': (
            'is_staff', 'is_superuser', 'is_active', 'groups',
            'user_permissions'
        )}),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    ordering = ('email',)

    actions = ['send_reset_password_email']

    def send_reset_password_email(self, request, queryset):
        """Действие для отправки письма о сбросе пароля."""
        for user in queryset:
            ResetUserPasswordUseCase().execute(user)

    send_reset_password_email.short_description = (
        "Отправить письмо о сбросе пароля"
    )
