import textwrap


class ShortDescriptionMixin:
    """Миксин, добавляющий модели сокращение для наименования."""

    description_field = 'description'
    placeholder = '...'
    max_width = 32

    def get_short_description(self):
        """Получить короткое наименование."""
        return textwrap.shorten(
            getattr(self, self.description_field),
            width=self.max_width,
            placeholder=self.placeholder
        )


class ModelAdminDisplayNameMixin:
    """Миксин для добавления в админ панель поля наименования объекта."""

    def display_name(self, obj):
        """Наименование экзамена."""
        return str(obj)

    display_name.short_description = "Наименование"
