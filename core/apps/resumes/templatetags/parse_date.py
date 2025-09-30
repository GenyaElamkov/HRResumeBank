from datetime import datetime

from django import template


register = template.Library()


# parse date
@register.filter
def parse_date(value: str) -> str | datetime:
    try:
        return datetime.strptime(value, '%Y-%m-%d')
    except (ValueError, TypeError):
        return value
