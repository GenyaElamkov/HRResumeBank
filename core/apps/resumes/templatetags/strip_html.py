import re

from django import template


register = template.Library()


@register.filter
def strip_html(value):
    return re.sub(r'<[^>]+>', '', str(value))
