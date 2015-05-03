from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def bank_account():
    return "BE23 7330 2625 4391"