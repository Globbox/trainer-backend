from os import path
import re

from django import template
from django.conf import settings
from markdown import markdown


register = template.Library()


@register.filter
def real_file_path(file_path):
    """Получить реальный путь к файлу."""
    cleaned_path = file_path.lstrip('/')
    return f'file://{path.join(settings.BASE_DIR.parent.parent, cleaned_path)}'


@register.filter
def with_markdown(markdown_string):
    """Добавить HTML теги для markdown полей."""
    clean = re.compile(r'</?p>')
    return re.sub(
        clean, '', markdown(
            markdown_string, extensions=[]
        )
    )
