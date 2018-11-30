from django import template
from django.contrib.auth.models import Group 

register = template.Library()

@register.simple_tag
def has_notification_appraisal(user,id):
	return user.user.hasNotificationAppraisal(id)

@register.simple_tag
def has_notification_comment(user,id):
	return user.user.hasNotificationComment(id)

@register.filter(name='has_group') 
def has_group(user, group_name):
    group =  Group.objects.get(name=group_name) 
    return group in user.groups.all()

@register.filter(name='has_group') 
def has_group_or_super(user, group_name):
    group =  Group.objects.get(name=group_name) 
    return group in user.groups.all() 