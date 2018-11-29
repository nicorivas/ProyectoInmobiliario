from django.views.generic import FormView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from user.views import userAppraisals
from appraisal.models import Appraisal, Comment
from django.contrib.auth.models import User
from user.views import appraiserWork, visadorWork

import reversion, datetime
from copy import deepcopy
from reversion.models import Version
from appraisal.forms import FormComment


def save_appraisalNF(appraisal, request, comment):
    print('save_appraisal')
    with reversion.create_revision():
        appraisal.save()
        reversion.set_user(request.user)
        reversion.set_comment(comment)
        return

def assign_tasadorNF(request):
    print(request.POST)
    pk = request.POST.dict()['tasadorAppraisal_id'];
    appraisal = Appraisal.objects.get(pk=pk)
    appraisal.tasadorUser = User.objects.get(pk=request.POST.dict()['tasador'])
    save_appraisalNF(appraisal, request,'Changed tasador')
    return

def assign_visadorNF(request):
    appraisal = Appraisal.objects.get(pk=request.POST.dict()['visadorAppraisal_id'])
    appraisal.visadorUser = User.objects.get(pk=request.POST.dict()['visador'])
    save_appraisalNF(appraisal, request,'Changed visador')
    return

@login_required(login_url='/user/login')
def main(request):

    if request.method == 'POST':
        print(request.POST)
        if 'delete' in request.POST:
            # Handle the delete button, next to every appraisal
            id = int(request.POST['appraisal_id'])
            appraisal = Appraisal.objects.get(pk=id)
            appraisal.delete()
        if 'btn_assign_tasador' in request.POST.keys():
            print(request.POST.dict())
            ret = assign_tasadorNF(request)
        if 'btn_assign_visador' in request.POST.keys():
            print(request.POST.dict())
            ret = assign_visadorNF(request)

    tasadores = User.objects.filter(groups__name__in=['tasador'])
    tasadores_info = appraiserWork(tasadores)

    visadores = User.objects.filter(groups__name__in=['visador'])
    visadores_info = visadorWork(visadores)

    # Get appraisals that this user can see

    appraisals_active, appraisals_finished = userAppraisals(request)

    # Form to create a comment

    form_comment = FormComment(label_suffix='')

    context = {
        'appraisals_active': appraisals_active,
        'appraisals_finished': appraisals_finished,
        'tasadores':tasadores_info,
        'visadores':visadores_info,
        'form_comment':form_comment}

    return render(request, 'main/index.html', context)

def logbook(request):
    '''
    Called when opening the logbook modal, through AJAX. Returns the comments of the relevant appraisal.
    '''
    id = int(request.GET['id'])

    appraisal = Appraisal.objects.get(id=id)
    comments = appraisal.comments.all().order_by('-timeCreated')

    return render(request,'main/logbook.html',{'appraisal':appraisal,'comments':comments})

def logbook_close(request):
    '''
    Called when closing the logbook modal, through AJAX.
    Deletes notifications.
    '''
    appraisal_id = int(request.GET['appraisal_id'])
    request.user.user.removeNotification(ntype="comment",appraisal_id=appraisal_id)

    return HttpResponse('')

def comment(request):
    '''
    Make a comment. This is an AJAX request called when the button comment is pressed.
    It should return the list of comments in logbook.html.
    '''
    id = int(request.POST['appraisal_id'])
    appraisal = Appraisal.objects.get(id=id)
    comment = Comment(
        user=request.user,
        text=request.POST['text'],
        event=int(request.POST['event']),
        timeCreated=datetime.datetime.now(datetime.timezone.utc),
        appraisal=appraisal)
    comment.save()

    appraisal.comments.add(comment)
    appraisal.save()

    comments = appraisal.comments.all().order_by('-timeCreated')

    # We need to add notifications to the relevant people. The tasador and visador of the appraisal,
    # and all other higher members like asignadores
    if appraisal.tasadorUser != None:
        if appraisal.tasadorUser != request.user: # dont add notifications to yourself
            appraisal.tasadorUser.user.addNotification(ntype="comment",appraisal_id=id,comment_id=comment.id)
    if appraisal.tasadorUser != None:
        if appraisal.visadorUser != request.user: # dont add notifications to yourself
            appraisal.visadorUser.user.addNotification(ntype="comment",appraisal_id=id,comment_id=comment.id)
    # add notifications to all asignadores
    appraisal.visadorUser.user.addNotification(ntype="comment",appraisal_id=id,comment_id=comment.id)

    asignadores = User.objects.filter(groups__name='asignador')
    for asignador in asignadores:
        if asignador != request.user: # dont add notifications to yourself
            asignador.user.addNotification(ntype="comment",appraisal_id=id,comment_id=comment.id)

    return render(request,'main/logbook.html',{'appraisal':appraisal,'comments':comments})

def delete_comment(request):
    '''
    Called from AJAX when the button of delete in all comments is pressed. It just deletes
    the comment and DOES NOT return a new list: the comment is just hidden via javascript
    and next time the logbook is loaded it just wont be there.
    '''

    comment_id = int(request.GET['comment_id'])
    comment = Comment.objects.get(id=comment_id)
    comment.delete()

    return JsonResponse({'comment_id':comment_id})
