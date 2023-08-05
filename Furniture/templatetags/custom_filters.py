# custom_filters.py

from django import template
from Furniture.models import FurnitureAd

register = template.Library()


@register.filter
def stars_range(value):
    return range(value)


@register.filter
def count_furniture_ads(category):
    return FurnitureAd.objects.filter(category=category).count()
