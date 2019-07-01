from django import template

register = template.Library()


@register.filter(name='get_split_0')
def get_split_0(value):
    return value.split("_")[0]


@register.filter(name='get_split_1')
def get_split_1(value):
    return value.split("_")[1]
