# custom_filters.py

from django import template

register = template.Library()


@register.filter
def stars_range(value):
    return range(value)
