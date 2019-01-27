from django.views.generic import FormView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from user.views import userAppraisals
from appraisal.models import Appraisal, Comment
from django.contrib.auth.models import User
from user.views import appraiserWork, visadorWork

import pytz
import json

import reversion, datetime
from copy import deepcopy
from reversion.models import Version
from appraisal.forms import FormComment

from evaluation.forms import EvaluationForm
from appraisal.models import AppraisalEvaluation

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
    
    #appraisals_not_assigned = appraisals_get_state(Appraisal.STATE_NOT_ASSIGNED)
    #appraisals_not_accepted = appraisals_get_state(Appraisal.STATE_NOT_ACCEPTED)
    #appraisals_in_appraisal = appraisals_get_state(Appraisal.STATE_IN_APPRAISAL)
    #appraisals_in_revision = appraisals_get_state(Appraisal.STATE_IN_REVISION)
    #appraisals_sent = appraisals_get_state(Appraisal.STATE_SENT)

    appraisals_not_assigned = []
    appraisals_not_accepted = []
    appraisals_in_appraisal = []
    appraisals_in_revision = []
    appraisals_sent = []
    appraisals = Appraisal.objects.select_related("real_estate_main__addressCommune","tasadorUser","visadorUser","property_main").all().order_by('timeCreated')
    for app in appraisals:
        if app.state == Appraisal.STATE_NOT_ASSIGNED:
            appraisals_not_assigned.append(app)
        elif app.state == Appraisal.STATE_NOT_ACCEPTED:
            appraisals_not_accepted.append(app)
        elif app.state == Appraisal.STATE_IN_APPRAISAL:
            appraisals_in_appraisal.append(app)
        elif app.state == Appraisal.STATE_IN_REVISION:
            appraisals_in_revision.append(app)
        elif app.state == Appraisal.STATE_SENT:
            appraisals_sent.append(app)

    # Form to create a comment

    form_comment = FormComment(label_suffix='')

    comment_mp = Comment.__dict__
    comment_dict = {}
    for k, v in comment_mp.items():
        if isinstance(v,type('')) or isinstance(v,type(1)):
            comment_dict[k] = v
    comment = json.dumps(comment_dict)
    print(comment)

    groups = request.user.groups.values_list('name',flat=True)

    context = {
        'evaluationForm': evaluationForm,
        'appraisals_not_assigned': appraisals_not_assigned,
        'appraisals_not_accepted': appraisals_not_accepted,
        'appraisals_in_appraisal': appraisals_in_appraisal,
        'appraisals_in_revision': appraisals_in_revision,
        'appraisals_sent': appraisals_sent,
        'form_comment':form_comment,
        'comment_class':comment,
        'groups':groups}

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




def appraisals_get_state(state):
    appraisals = Appraisal.objects.select_related("real_estate_main__addressCommune","tasadorUser","visadorUser").filter(state=state).order_by('timeCreated')
    return appraisals

def ajax_assign_tasador_modal(request):
    '''
    Assign a tasador from an appraisal. Gets called through AJAX when clicked
    on the corresponding modal, which has a form where you can select the user.
    '''
    appraisal = Appraisal.objects.get(id=int(request.GET['appraisal_id']))
    tasadores = User.objects.filter(groups__name__in=['tasador']).order_by('last_name')
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
    appraisal_id = int(request.POST['appraisal_id'])
    tasador_id = int(request.POST['tasador'])

    appraisal = Appraisal.objects.get(id=appraisal_id)
    tasador = User.objects.get(id=tasador_id)
    user = request.user

    appraisal.tasadorUser = tasador
    
    comment = appraisal.addComment(Comment.EVENT_TASADOR_SOLICITADO,user,datetime.datetime.now(datetime.timezone.utc),
        text="Tasación solicitada a "+tasador.first_name +' '+ tasador.last_name)
    
    appraisal.tasadorUser.user.addNotification(ntype="comment",appraisal_id=appraisal_id,comment_id=comment.id)
    appraisal.state = Appraisal.STATE_NOT_ACCEPTED
    appraisal.save()

    appraisals_not_accepted = appraisals_get_state(Appraisal.STATE_NOT_ACCEPTED)
    
    return render(request,'main/appraisals_not_accepted.html',{'appraisals_not_accepted':appraisals_not_accepted})

def ajax_assign_visador(request):
    '''
    Assign a visador from an appraisal. Gets called through AJAX when clicked
    on the corresponding modal, which has a form where you can select the user.
    Button an be called from two tables, so different appraisals must be gotten
    to modify the correct table.
    '''
    appraisal_id = int(request.POST['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)
    visador_id = int(request.POST['visador'])
    visador = User.objects.get(id=visador_id)
    user_id = int(request.user.id)
    user = User.objects.get(id=user_id)
    if appraisal.visadorUser == visador:
        status = "Visador ya seleccionado"
    else:
        appraisal.visadorUser = visador
        appraisal.addComment(Comment.EVENT_VISADOR_ASIGNADO,user,datetime.datetime.now(datetime.timezone.utc),
            text="Visación asignada a "+visador.user.first_name + ' ' + visador.user.last_name)
        appraisal.save()
        status = ""

    if request.POST['source_table'] == 'table_not_assigned':
        appraisals_not_assigned = appraisals_get_state(Appraisal.STATE_NOT_ASSIGNED)
        return render(request,'main/appraisals_not_assigned.html',{'appraisals_not_assigned':appraisals_not_assigned,'status':status})
    elif request.POST['source_table'] == 'table_active':
        appraisals_active = appraisals_get_state(Appraisal.STATE_IN_APPRAISAL)
        return render(request,'main/appraisals_active.html',{'appraisals_active':appraisals_active,'status':status})

def ajax_unassign_tasador(request):
    '''
    Unassign a tasador from an appraisal. Gets called through AJAX when clicked
    on the corresponding confirmation modal.
    '''
    appraisal_id = int(request.GET['appraisal_id'])
    user_id = int(request.user.id)

    appraisal = Appraisal.objects.get(id=appraisal_id)
    tasador = appraisal.tasadorUser
    appraisal.tasadorUser = None
    appraisal.state = Appraisal.STATE_NOT_ASSIGNED
    user = User.objects.get(id=user_id)
    appraisal.addComment(Comment.EVENT_TASADOR_DESASIGNADO,user,datetime.datetime.now(datetime.timezone.utc),
        text="Tasador "+tasador.user.full_name+" fue desasignado.")
    appraisal.save()
    appraisals_not_assigned = appraisals_get_state(Appraisal.STATE_NOT_ASSIGNED)
    return render(request,'main/appraisals_not_assigned.html',{'appraisals_not_assigned':appraisals_not_assigned})

def ajax_unassign_visador(request):
    '''
    Unassign a tasador from an appraisal. Gets called through AJAX when clicked
    on the corresponding confirmation modal.
    '''
    appraisal_id = int(request.GET['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)
    visador_id = int(request.user.id)
    visador = appraisal.tasadorUser
    appraisal.visadorUser = None
    user = User.objects.get(id=user_id)
    appraisal.addComment(Comment.EVENT_VISADOR_DESASIGNADO,user,datetime.datetime.now(datetime.timezone.utc),
        text="Visador "+visador.user.full_name+" fue desasignado.")
    appraisal.save()

    appraisals_active = appraisals_get_state(Appraisal.STATE_IN_APPRAISAL)

    return render(request,'main/appraisals_active.html',{'appraisals_active':appraisals_active})

def ajax_accept_appraisal(request):

    appraisal_id = int(request.POST['appraisal_id'])
    text = request.POST['text']

    appraisal = Appraisal.objects.get(id=appraisal_id)
    appraisal.state = Appraisal.STATE_IN_APPRAISAL
    appraisal.addComment(Comment.EVENT_SOLICITUD_ACEPTADA,request.user,datetime.datetime.now(datetime.timezone.utc),text=text)
    appraisal.save()

    appraisals_in_appraisal = appraisals_get_state(Appraisal.STATE_IN_APPRAISAL)

    return render(request,'main/appraisals_in_appraisal.html',{'appraisals_in_appraisal':appraisals_in_appraisal})

def ajax_reject_appraisal(request):

    appraisal_id = int(request.POST['appraisal_id'])
    text = request.POST['text']

    appraisal = Appraisal.objects.get(id=appraisal_id)
    appraisal.state = Appraisal.STATE_NOT_ASSIGNED
    appraisal.tasadorUser = None
    appraisal.save()

    appraisal.addComment(Comment.EVENT_SOLICITUD_RECHAZADA,request.user,datetime.datetime.now(datetime.timezone.utc),text=text)

    appraisals_not_assigned = appraisals_get_state(Appraisal.STATE_NOT_ASSIGNED)

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
    appraisal_id = int(request.GET['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)
    comments = appraisal.comments.all().order_by('-timeCreated')
    form_comment = FormComment(label_suffix='')
    
    table = request.GET['table']
    form_comment.fields['event'].choices = appraisal.getCommentChoices(comments,state=appraisal.state)

    return render(request,'main/logbook.html',{'appraisal':appraisal,'comments':comments,'form_comment':form_comment})

def ajax_logbook_close(request):
    '''
    Called when closing the logbook modal, through AJAX.
    1. Deletes notifications.
    2. Saves modified variables
    '''
    appraisal_id = int(request.POST['appraisal_id'])
    request.user.user.removeNotification(ntype="comment",appraisal_id=appraisal_id)

    appraisal = Appraisal.objects.get(id=appraisal_id)
    if request.POST['contacto'] in ["None",""]:
        appraisal.contacto = None
    else:
        appraisal.contacto = request.POST['contacto']
    if request.POST['contactoEmail'] in ["None",""]:
        appraisal.contactoEmail = None
    else:
        appraisal.contactoEmail = request.POST['contactoEmail']
    if request.POST['contactoTelefono'] in ["None",""]:
        appraisal.contactoTelefono = None
    else:
        appraisal.contactoTelefono = request.POST['contactoTelefono']
    if request.POST['cliente'] in ["None",""]:
        appraisal.cliente = None
    else:
        appraisal.cliente = request.POST['cliente']
    if request.POST['clienteEmail'] in ["None",""]:
        appraisal.clienteEmail = None
    else:
        appraisal.clienteEmail = request.POST['clienteEmail']
    if request.POST['clienteTelefono'] in ["None",""]:
        appraisal.clienteTelefono = None
    else:
        appraisal.clienteTelefono = request.POST['clienteTelefono']
    appraisal.save()

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
    event = int(request.POST['event'])
    
    if event == Comment.EVENT_VISITA_ACORDADA:
        text = "Visita agendada para "+request.POST['datetime']+". "+request.POST['text']
    elif event == Comment.EVENT_PROPIEDAD_VISITADA:
        text = "Propiedad visitada el "+request.POST['datetime']+". "+request.POST['text']
    else:
        text = request.POST['text']

    if event == Comment.EVENT_INCIDENCIA:
        appraisal.in_conflict = True
        appraisal.save()
    elif event == Comment.EVENT_ENVIADA_A_VISADOR:
        appraisal.state = Appraisal.STATE_IN_REVISION
        appraisal.save()
    elif event == Comment.EVENT_ENTREGADO_AL_CLIENTE:
        appraisal.state = Appraisal.STATE_SENT
        appraisal.timeFinished = datetime.datetime.now(pytz.utc)
        appraisal.save()

    comment = appraisal.addComment(int(request.POST['event']),request.user,datetime.datetime.now(datetime.timezone.utc),text)

    comments = appraisal.comments.all().order_by('-timeCreated')

    form_comment = FormComment(label_suffix='')
    form_comment.fields['event'].choices = appraisal.getCommentChoices(comments,state=appraisal.state)

    # We need to add notifications to the relevant people. The tasador and visador of the appraisal,
    # and all other higher members like asignadores
    if appraisal.tasadorUser != None:
        if appraisal.tasadorUser != request.user: # dont add notifications to yourself
            appraisal.tasadorUser.user.addNotification(ntype="comment",appraisal_id=id,comment_id=comment.id)
    if appraisal.visadorUser != None:
        if appraisal.visadorUser != request.user: # dont add notifications to yourself
            appraisal.visadorUser.user.addNotification(ntype="comment",appraisal_id=id,comment_id=comment.id)
    # add notifications to all asignadores
    # appraisal.visadorUser.user.addNotification(ntype="comment",appraisal_id=id,comment_id=comment.id)

    asignadores = User.objects.filter(groups__name='asignador')
    for asignador in asignadores:
        if asignador != request.user: # dont add notifications to yourself
            asignador.user.addNotification(ntype="comment",appraisal_id=id,comment_id=comment.id)

    return render(request,'main/comment.html',{'comment':comment})

def ajax_delete_comment(request):
    '''
    Called from AJAX when the button of delete in all comments is pressed. It just deletes
    the comment and DOES NOT return a new list: the comment is just hidden via javascript
    and next time the logbook is loaded it just wont be there.
    '''
    appraisal_id = int(request.GET['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)

    comment_id = int(request.GET['comment_id'])
    comment = Comment.objects.get(id=comment_id)
    if comment.event == Comment.EVENT_CLIENTE_VALIDADO:
        appraisal.clienteValidado = False
        appraisal.save()
    elif comment.event == Comment.EVENT_CONTACTO_VALIDADO:
        appraisal.contactoValidado = False
        appraisal.save()
    elif comment.event == Comment.EVENT_ENTREGADO_AL_CLIENTE:
        appraisal.state = Appraisal.STATE_IN_REVISION
        appraisal.timeFinished = None
        appraisal.save()
    comment.delete()

    form_comment = FormComment(label_suffix='')
    choices = appraisal.getCommentChoices(state=appraisal.state)

    return JsonResponse({'comment_id':comment_id,'choices':choices})

def ajax_finish_appraisal(request):
    appraisal_id = int(request.GET['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)
    appraisal.state = Appraisal.STATE_FINISHED
    appraisal.timeFinished = datetime.datetime.now(pytz.utc)
    appraisal.save()
    appraisals_finished = appraisals_get_finished(request.user)
    return render(request,'main/appraisals_finished.html',{'appraisals_finished': appraisals_finished})

def ajax_unfinish_appraisal(request):
    appraisal_id = int(request.GET['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)
    appraisal.state = Appraisal.STATE_ACTIVE
    appraisal.save()
    appraisals_active = appraisals_get_active(request.user)
    return render(request,'main/appraisals_active.html',{'appraisals_active': appraisals_active})

def ajax_validate_cliente(request):
    appraisal_id = int(request.GET['appraisal_id'])
    t = int(request.GET['type'])
    appraisal = Appraisal.objects.get(id=appraisal_id)
    if t == 1:
        if appraisal.clienteValidado:
            appraisal.clienteValidado = False
            comment = appraisal.addComment(Comment.EVENT_CLIENTE_INVALIDADO,request.user,datetime.datetime.now(datetime.timezone.utc))
        else:
            appraisal.clienteValidado = True
            comment = appraisal.addComment(Comment.EVENT_CLIENTE_VALIDADO,request.user,datetime.datetime.now(datetime.timezone.utc))
    elif t == 2:
        if appraisal.contactoValidado:
            appraisal.contactoValidado = False
            comment = appraisal.addComment(Comment.EVENT_CONTACTO_INVALIDADO,request.user,datetime.datetime.now(datetime.timezone.utc))
        else:
            appraisal.contactoValidado = True
            comment = appraisal.addComment(Comment.EVENT_CONTACTO_VALIDADO,request.user,datetime.datetime.now(datetime.timezone.utc))
    appraisal.save()
    return render(request,'main/comment.html',{'comment':comment})

def ajax_unvalidate_cliente(request):
    appraisal_id = int(request.GET['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)
    t = 1
    if t == 1:
        appraisal.clienteValidado = False
    elif t == 2:
        appraisal.contactoValidado = False
    appraisal.save()
    return JsonResponse({})

def ajax_get_appraisal_row(request):
    appraisal_id = int(request.GET['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)

    table = request.GET['table']
    
    return render(request,'main/appraisals_'+table+'_tr.html',{'appraisal':appraisal})
