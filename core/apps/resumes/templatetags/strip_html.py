import html
import re

from django import template
from django.utils.html import strip_tags


register = template.Library()


@register.filter
def strip_html(value: str) -> str:
    """
    Полностью удаляет весь HTML, CSS и их атрибуты, лишние пробелы схлопываются.
    Теги полностью удаляются, не заменяя их на пробелы.
    """
    if not value:
        return ''
    stripped = strip_tags(str(value))
    # Декодируем HTML-сущности
    text = html.unescape(stripped)
    # Удаляем лишние пробелы
    text = re.sub(r'\s+', ' ', text.strip())

    return text
