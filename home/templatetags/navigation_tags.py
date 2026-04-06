from django import template
from home.models import GlobalHeader

register = template.Library()

@register.inclusion_tag('includes/header_component.html', takes_context=True)
def get_global_header(context):
    header = GlobalHeader.objects.first()
    return {
        'header': header,
        'request': context.get('request'),
    }