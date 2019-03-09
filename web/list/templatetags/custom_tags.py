from django import template
from django.contrib.auth.models import Group 
import os

register = template.Library()

@register.simple_tag
def has_notification_appraisal(appraisal_id,notification_ids):
	return appraisal_id in notification_ids

@register.simple_tag
def has_notification_comment(comment_id,notification_ids):
	return comment_id in notification_ids

@register.filter(name='has_group') 
def has_group(user, group_name):
    group =  Group.objects.get(name=group_name) 
    return group in user.groups.all()

@register.filter(name='has_group') 
def has_group_or_super(user, group_name):
    group =  Group.objects.get(name=group_name) 
    return group in user.groups.all() 

@register.filter
def filename(value):
    return os.path.basename(value.file.name)