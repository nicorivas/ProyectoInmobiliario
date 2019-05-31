from django import template

register = template.Library()

@register.inclusion_tag('base/header.html')
def show_header(title):
    return {"title":title}