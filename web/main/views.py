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

from evaluation.forms import EvaluationForm
from appraisal.models import AppraisalEvaluation


def assign_tasador(appraisal_id,tasador_id,user_id):
    appraisal = Appraisal.objects.get(id=appraisal_id)
    tasador = User.objects.get(id=tasador_id)
    user = User.objects.get(id=user_id)

    appraisal.tasadorUser = tasador
    appraisal.tasadorUser.user.addNotification(ntype="comment",appraisal_id=id,comment_id=comment.id)
    appraisal.addComment(Comment.EVENT_TASADOR_SOLICITADO,user,datetime.datetime.now(datetime.timezone.utc),
        text="Tasación solicitada a "+tasador.user.full_name)
    return

def unassign_tasador(appraisal_id,user_id):
    appraisal = Appraisal.objects.get(id=appraisal_id)
    tasador = appraisal.tasadorUser
    appraisal.tasadorUser = None
    appraisal.state = Appraisal.STATE_NOTASSIGNED
    user = User.objects.get(id=user_id)
    appraisal.addComment(Comment.EVENT_TASADOR_DESASIGNADO,user,datetime.datetime.now(datetime.timezone.utc),
        text="Tasador "+tasador.user.full_name+" fue desasignado.")
    appraisal.save()
    return

def assign_visador(appraisal_id,visador_id,user_id):
    appraisal = Appraisal.objects.get(id=appraisal_id)
    visador = User.objects.get(id=visador_id)
    user = User.objects.get(id=user_id)
    if appraisal.visadorUser == visador:
        return "Visador ya seleccionado"
    else:
        appraisal.visadorUser = visador
        appraisal.addComment(Comment.EVENT_VISADOR_ASIGNADO,user,datetime.datetime.now(datetime.timezone.utc),
            text="Visación asignada a "+visador.user.full_name)
        appraisal.save()
        return ""

def unassign_visador(appraisal_id):
    appraisal = Appraisal.objects.get(id=appraisal_id)
    visador = appraisal.tasadorUser
    appraisal.visadorUser = None
    user = User.objects.get(id=user_id)
    appraisal.addComment(Comment.EVENT_VISADOR_DESASIGNADO,user,datetime.datetime.now(datetime.timezone.utc),
        text="Visador "+visador.user.full_name+" fue desasignado.")
    appraisal.save()
    return

@login_required(login_url='/user/login')
def main(request):
    evaluationForm = EvaluationForm()
    if request.method == 'POST':
        if 'evaluadorAppraisal_id' in request.POST.keys():
            evaluationForm = EvaluationForm(request.POST)
            if evaluationForm.is_valid():
                _onTime = evaluationForm.cleaned_data['onTime']
                _completeness = evaluationForm.cleaned_data['completeness']
                _generalQuality = evaluationForm.cleaned_data['generalQuality']
                _correctSurface = evaluationForm.cleaned_data['correctSurface']
                _homologatedReferences = evaluationForm.cleaned_data['homologatedReferences']
                _completeNormative = evaluationForm.cleaned_data['completeNormative']
                _commentText = evaluationForm.cleaned_data['commentText']
                _commentFeedback = evaluationForm.cleaned_data['commentFeedback']
                appraisal = Appraisal.objects.get(pk=request.POST['evaluadorAppraisal_id'])
                appraiser = User.objects.get(pk=request.POST['evaluador_id'])
                evaluation, created = AppraisalEvaluation.objects.update_or_create(
                                        appraisal=appraisal,
                                        #user=appraiser,
                                        defaults={
                                            "appraisal":appraisal,
                                            'user':appraiser,
                                            'onTime':_onTime,
                                            'completeness':_completeness,
                                            'generalQuality':_generalQuality,
                                            'correctSurface': _correctSurface ,
                                            'completeNormative': _completeNormative,
                                            'homologatedReferences': _homologatedReferences,
                                            'commentText':_commentText,
                                            'commentFeedback':_commentFeedback})
                #evaluationForm.save()
                print(evaluation.evaluationResult)

    # Get appraisals that this user can see
    #appraisals_not_assigned, appraisals_active, appraisals_finished = userAppraisals(request)
    appraisals_not_assigned = appraisals_get_not_assigned(request.user)
    appraisals_not_accepted = appraisals_get_not_accepted(request.user)
    appraisals_active = appraisals_get_active(request.user)
    appraisals_finished = appraisals_get_finished(request.user)
    appraisals_imported = appraisals_get_imported(request.user)

    # Form to create a comment

    form_comment = FormComment(label_suffix='')

    context = {
        'evaluationForm': evaluationForm,
        'appraisals_not_assigned': appraisals_not_assigned,
        'appraisals_not_accepted': appraisals_not_accepted,
        'appraisals_active': appraisals_active,
        'appraisals_finished': appraisals_finished,
        'appraisals_imported': appraisals_imported,
        'form_comment':form_comment}

    return render(request, 'main/index.html', context)

@login_required(login_url='/user/login')
def imported_appraisals(request):
    evaluationForm = EvaluationForm()
    if request.method == 'POST':
        if 'evaluadorAppraisal_id' in request.POST.keys():
            evaluationForm = EvaluationForm(request.POST)
            if evaluationForm.is_valid():
                _onTime = evaluationForm.cleaned_data['onTime']
                _completeness = evaluationForm.cleaned_data['completeness']
                _generalQuality = evaluationForm.cleaned_data['generalQuality']
                _correctSurface = evaluationForm.cleaned_data['correctSurface']
                _homologatedReferences = evaluationForm.cleaned_data['homologatedReferences']
                _completeNormative = evaluationForm.cleaned_data['completeNormative']
                _commentText = evaluationForm.cleaned_data['commentText']
                _commentFeedback = evaluationForm.cleaned_data['commentFeedback']
                appraisal = Appraisal.objects.get(pk=request.POST['evaluadorAppraisal_id'])
                appraiser = User.objects.get(pk=request.POST['evaluador_id'])
                evaluation, created = AppraisalEvaluation.objects.update_or_create(
                                        appraisal=appraisal,
                                        #user=appraiser,
                                        defaults={
                                            "appraisal":appraisal,
                                            'user':appraiser,
                                            'onTime':_onTime,
                                            'completeness':_completeness,
                                            'generalQuality':_generalQuality,
                                            'correctSurface': _correctSurface ,
                                            'completeNormative': _completeNormative,
                                            'homologatedReferences': _homologatedReferences,
                                            'commentText':_commentText,
                                            'commentFeedback':_commentFeedback})
                #evaluationForm.save()
                print(evaluation.evaluationResult)

    # Get appraisals that this user can see
    #appraisals_not_assigned, appraisals_active, appraisals_finished = userAppraisals(request)
    appraisals_imported = appraisals_get_imported(request.user)


    context = {
        'evaluationForm': evaluationForm,
        'appraisals_imported': appraisals_imported}

    return render(request, 'main/appraisals_imported.html', context)






def appraisals_get_not_assigned(user):
    appraisals = Appraisal.objects.select_related().filter(state=Appraisal.STATE_NOTASSIGNED)
    appraisals_not_assigned = appraisals.filter(tasadorUser__isnull=True).order_by('timeCreated')
    appraisals_not_assigned.only(
        "id",
        "timeCreated",
        "timeDue",
        "state",
        "tipoTasacion",
        "solicitante",
        "solicitanteCodigo",
        "tasadorUser",
        "visadorUser",
        "realEstate__addressStreet",
        "realEstate__addressNumber",
        "realEstate__addressCommune__name")
    return appraisals_not_assigned

def appraisals_get_not_accepted(user):
    appraisals = Appraisal.objects.select_related().filter(state=Appraisal.STATE_NOTASSIGNED)
    appraisals_not_accepted = appraisals.filter(tasadorUser__isnull=False).order_by('timeCreated').order_by('timeCreated')
    if not user.is_superuser:
        appraisals_not_accepted = appraisals_not_accepted.filter(Q(tasadorUser=user)|Q(visadorUser=user))
    appraisals_not_accepted.select_related().only(
        "id",
        "timeCreated",
        "timeDue",
        "state",
        "tipoTasacion",
        "solicitante",
        "solicitanteCodigo",
        "tasadorUser",
        "visadorUser",
        "realEstate__addressStreet",
        "realEstate__addressNumber",
        "realEstate__addressCommune__name")
    return appraisals_not_accepted

def appraisals_get_active(user):
    appraisals_active = Appraisal.objects.select_related().filter(state=Appraisal.STATE_ACTIVE).order_by('timeCreated')
    if not user.is_superuser:
        appraisals_active = appraisals_active.filter(Q(tasadorUser=user)|Q(visadorUser=user))
    appraisals_active.select_related().only(
        "id",
        "timeCreated",
        "timeDue",
        "state",
        "tipoTasacion",
        "solicitante",
        "solicitanteCodigo",
        "tasadorUser",
        "visadorUser",
        "realEstate__addressStreet",
        "realEstate__addressNumber",
        "realEstate__addressCommune__name")
    return appraisals_active

def appraisals_get_finished(user):
    appraisals_finished = Appraisal.objects.select_related().filter(state=Appraisal.STATE_FINISHED).order_by('timeCreated')
    if not user.is_superuser:
        appraisals_finished = appraisals_finished.filter(Q(tasadorUser=user)|Q(visadorUser=user))
    appraisals_finished.select_related().only(
        "id",
        "timeCreated",
        "timeDue",
        "state",
        "tipoTasacion",
        "solicitante",
        "solicitanteCodigo",
        "tasadorUser",
        "visadorUser",
        "realEstate__addressStreet",
        "realEstate__addressNumber",
        "realEstate__addressCommune__name")
    return appraisals_finished

def appraisals_get_imported(user):
    appraisals_imported = Appraisal.objects.select_related().filter(state=Appraisal.STATE_IMPORTED).order_by('timeCreated')
    if not user.is_superuser:
        appraisals_imported = appraisals_imported.filter(Q(tasadorUser=user)|Q(visadorUser=user))
    appraisals_imported.select_related().only(
        "id",
        "timeCreated",
        "timeDue",
        "state",
        "tipoTasacion",
        "solicitante",
        "solicitanteCodigo",
        "tasadorUser",
        "visadorUser",
        "realEstate__addressStreet",
        "realEstate__addressNumber",
        "realEstate__addressCommune__name")
    print(appraisals_imported)
    return appraisals_imported

def ajax_assign_tasador_modal(request):
    '''
    Assign a tasador from an appraisal. Gets called through AJAX when clicked
    on the corresponding modal, which has a form where you can select the user.
    '''
    appraisal = Appraisal.objects.get(id=int(request.GET['appraisal_id']))
    tasadores = User.objects.filter(groups__name__in=['tasador'])
    tasadores_info = appraiserWork(tasadores)
    return render(request,'main/modals_assign_tasador.html',
        {'appraisal':appraisal,
         'tasadores':tasadores_info})

def ajax_assign_visador_modal(request):
    '''
    Assign a tasador from an appraisal. Gets called through AJAX when clicked
    on the corresponding modal, which has a form where you can select the user.
    '''
    appraisal = Appraisal.objects.get(id=int(request.GET['appraisal_id']))
    visadores = User.objects.filter(groups__name__in=['visador'])
    visadores_info = visadorWork(visadores)
    return render(request,'main/modals_assign_visador.html',
        {'appraisal':appraisal,
         'visadores':visadores_info})


def ajax_assign_tasador(request):
    '''
    Assign a tasador from an appraisal. Gets called through AJAX when clicked
    on the corresponding modal, which has a form where you can select the user.
    '''
    assign_tasador(int(request.POST['appraisal_id']),int(request.POST['tasador']),int(request.user.id))
    appraisals_not_accepted = appraisals_get_not_accepted(request.user)
    return render(request,'main/appraisals_not_accepted.html',
        {'appraisals_not_accepted':appraisals_not_accepted})

def ajax_assign_visador(request):
    '''
    Assign a visador from an appraisal. Gets called through AJAX when clicked
    on the corresponding modal, which has a form where you can select the user.
    Button an be called from two tables, so different appraisals must be gotten
    to modify the correct table.
    '''
    status = assign_visador(int(request.POST['appraisal_id']),int(request.POST['visador']),int(request.user.id))
    if request.POST['source_table'] == 'table_not_assigned':
        appraisals_not_assigned = appraisals_get_not_assigned(request.user)
        return render(request,'main/appraisals_not_assigned.html',{'appraisals_not_assigned':appraisals_not_assigned,'status':status})
    elif request.POST['source_table'] == 'table_active':
        appraisals_active = appraisals_get_active(request.user)
        return render(request,'main/appraisals_active.html',{'appraisals_active':appraisals_active,'status':status})

def ajax_unassign_tasador(request):
    '''
    Unassign a tasador from an appraisal. Gets called through AJAX when clicked
    on the corresponding confirmation modal.
    '''
    unassign_tasador(int(request.GET['appraisal_id']),int(request.user.id))
    appraisals_not_assigned = appraisals_get_not_assigned(request.user)
    return render(request,'main/appraisals_not_assigned.html',{'appraisals_not_assigned':appraisals_not_assigned})

def ajax_unassign_visador(request):
    '''
    Unassign a tasador from an appraisal. Gets called through AJAX when clicked
    on the corresponding confirmation modal.
    '''
    unassign_visador(int(request.GET['appraisal_id']),int(request.user.id))

    appraisals_active = appraisals_get_active(request.user)

    return render(request,'main/appraisals_active.html',{'appraisals_active':appraisals_active})

def ajax_accept_appraisal(request):

    appraisal_id = int(request.POST['appraisal_id'])
    text = request.POST['text']

    appraisal = Appraisal.objects.get(id=appraisal_id)
    appraisal.state = Appraisal.STATE_ACTIVE
    appraisal.addComment(Comment.EVENT_SOLICITUD_ACEPTADA,request.user,datetime.datetime.now(datetime.timezone.utc),text=text)

    appraisals_active = appraisals_get_active(request.user)

    return render(request,'main/appraisals_active.html',{'appraisals_active':appraisals_active})

def ajax_reject_appraisal(request):

    appraisal_id = int(request.POST['appraisal_id'])
    text = request.POST['text']

    appraisal = Appraisal.objects.get(id=appraisal_id)
    appraisal.state = Appraisal.STATE_NOTASSIGNED
    appraisal.tasadorUser = None
    appraisal.save()

    appraisal.addComment(Comment.EVENT_SOLICITUD_RECHAZADA,request.user,datetime.datetime.now(datetime.timezone.utc),text=text)

    appraisals_not_assigned = appraisals_get_not_assigned(request.user)

    return render(request,'main/appraisals_not_assigned.html',{'appraisals_not_assigned':appraisals_not_assigned})

def ajax_delete_appraisal(request):
    # Handle the delete button, next to every appraisal
    id = int(request.GET['appraisal_id'])
    appraisal = Appraisal.objects.get(pk=id)
    appraisal.delete()
    return HttpResponse('')

def ajax_logbook(request):
    '''
    Called when opening the logbook modal, through AJAX. Returns the comments of the relevant appraisal.
    '''
    id = int(request.GET['id'])

    appraisal = Appraisal.objects.get(id=id)
    comments = appraisal.comments.all().order_by('-timeCreated')
    form_comment = FormComment(label_suffix='')
    form_comment.fields['event'].choices = appraisal.getCommentChoices(comments)

    return render(request,'main/logbook.html',{'appraisal':appraisal,'comments':comments,'form_comment':form_comment})

def ajax_logbook_close(request):
    '''
    Called when closing the logbook modal, through AJAX. Deletes notifications.
    '''
    appraisal_id = int(request.GET['appraisal_id'])
    request.user.user.removeNotification(ntype="comment",appraisal_id=appraisal_id)

    return HttpResponse('')

def ajax_logbook_change_event(request):
    '''
    '''

    #if request['event'] == 

    return JsonResponse({'comment_id':comment_id})

def ajax_comment(request):
    '''
    Make a comment. This is an AJAX request called when the button comment is pressed.
    It should return the list of comments in logbook.html.
    '''
    id = int(request.POST['appraisal_id'])

    appraisal = Appraisal.objects.get(id=id)
    if request.POST['datetime'] == "":
        text = request.POST['text']
    else:
        text = "Visita agendada para "+request.POST['datetime']+". "+request.POST['text']
    comment = appraisal.addComment(int(request.POST['event']),request.user,datetime.datetime.now(datetime.timezone.utc),text)

    comments = appraisal.comments.all().order_by('-timeCreated')

    form_comment = FormComment(label_suffix='')
    form_comment.fields['event'].choices = appraisal.getCommentChoices(comments)

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

    return render(request,'main/logbook.html',{'appraisal':appraisal,'comments':comments,'form_comment':form_comment})

def ajax_delete_comment(request):
    '''
    Called from AJAX when the button of delete in all comments is pressed. It just deletes
    the comment and DOES NOT return a new list: the comment is just hidden via javascript
    and next time the logbook is loaded it just wont be there.
    '''

    comment_id = int(request.GET['comment_id'])
    comment = Comment.objects.get(id=comment_id)
    comment.delete()

    appraisal_id = int(request.GET['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)

    form_comment = FormComment(label_suffix='')
    choices = appraisal.getCommentChoices()

    return JsonResponse({'comment_id':comment_id,'choices':choices})
