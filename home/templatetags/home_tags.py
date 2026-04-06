from django import template
from home.models import GlobalHeader

register =  template.Library()


@register.simple_tag
def get_global_header():

    return GlobalHeader.objects.first()
