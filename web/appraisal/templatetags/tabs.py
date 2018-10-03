from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def tab_nav_aria_selected(value, arg):
    print('value={}-'.format(value))
    print('arg={}-'.format(arg))
    if value == arg:
        return 'true'
    elif value == '' and arg == 'general':
        return 'true'
    else:
        return 'false'

@register.filter
@stringfilter
def tab_nav_class(value, arg):
    if value == arg:
        return 'nav-link active'
    elif value == '' and arg == 'general':
        return 'nav-link active'
    else:
        return 'nav-link'

@register.filter
@stringfilter
def tab_pane_class(value, arg):
    if value == arg:
        return 'tab-pane fade show active'
    elif value == '' and arg == 'general':
        return 'tab-pane fade show active'
    else:
        return 'tab-pane fade'
