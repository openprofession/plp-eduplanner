# encoding: utf-8

from django import template

register = template.Library()


@register.filter
def get_by_index(dictionary, key):
    return dictionary.get(key, False)
