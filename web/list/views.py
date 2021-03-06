import datetime
import pytz
import json
from django.views.generic import FormView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from user.views import userAppraisals
from appraisal.models import Appraisal, Comment, Report, AppraiserExpenses
from django.contrib.auth.models import User
from user.views import appraiserWork, visadorWork
from django.utils import timezone

from copy import deepcopy
from reversion.models import Version
from appraisal.forms import FormExpenses
from .forms import TasadorSearch

from evaluation.forms import EvaluationForm
from appraisal.models import AppraisalEvaluation
from create.forms import AppraisalCreateForm
from commune.models import Commune
from region.models import Region
from appraisal.data import getAppraisalFromRequest

'''To avoid database problems with time zone, timezone has to be set when date is submitted to the database, postgres 
server will translate the date to UTC (example: date sent=2019-12-1 12:00 -03:00, in server=2019-12-1 15:00 +00)
then at the frontend Django will translate to timezone set in settings.py. 
So to sent date to database use: datime.datetime.now(pytz.timezone('timezone")). 
Caution: don't use timezone when comparing dates with datetime.datetime.now()
'''
timezone_cl = pytz.timezone('Chile/Continental')

def get_appraisals_not_assigned(request,appraisals):
    appraisals_not_assigned = []
    for app in appraisals:
        if app.state == Appraisal.STATE_NOT_ASSIGNED:
            if app.tasadorUser == request.user or \
               app.visadorUser == request.user or \
               request.user.is_superuser or \
               request.user.groups.filter(name='asignador').exists():
                appraisals_not_assigned.append(app)
    return appraisals_not_assigned

def get_appraisals_not_accepted(request,appraisals):
    appraisals_not_accepted = []
    for app in appraisals:
        if app.state == Appraisal.STATE_NOT_ACCEPTED:
            if app.tasadorUser == request.user or \
               app.visadorUser == request.user or \
               request.user.is_superuser or \
               request.user.groups.filter(name='asignador').exists():
                appraisals_not_accepted.append(app)
    return appraisals_not_accepted

def get_appraisals_in_appraisal(request,appraisals):
    appraisals_in_appraisal = []
    for app in appraisals:
        if app.state == Appraisal.STATE_IN_APPRAISAL:
            if app.tasadorUser == request.user or \
               app.visadorUser == request.user or \
               request.user.is_superuser or \
               request.user.groups.filter(name='asignador').exists():
                appraisals_in_appraisal.append(app)
    return appraisals_in_appraisal

def get_appraisals_in_revision(request,appraisals):
    appraisals_in_revision = []
    for app in appraisals:
        if app.state == Appraisal.STATE_IN_REVISION:
            if app.tasadorUser == request.user or \
               app.visadorUser == request.user or \
               request.user.is_superuser or \
               request.user.groups.filter(name='asignador').exists():
                appraisals_in_revision.append(app)
    return appraisals_in_revision

def get_appraisals_sent(request,appraisals):
    appraisals_sent = []
    for app in appraisals:
        if app.state == Appraisal.STATE_SENT:
            if app.tasadorUser == request.user or \
               app.visadorUser == request.user or \
               request.user.is_superuser or \
               request.user.groups.filter(name='asignador').exists():
                appraisals_sent.append(app)
    return appraisals_sent

def get_appraisals_returned(request,appraisals):
    appraisals_returned = []
    for app in appraisals:
        if app.state == Appraisal.STATE_RETURNED:
            if app.tasadorUser == request.user or \
               app.visadorUser == request.user or \
               request.user.is_superuser or \
               request.user.groups.filter(name='asignador').exists():
                appraisals_returned.append(app)
    return appraisals_returned

@login_required(login_url='/user/login')
def main(request):

    # Get appraisals that this user can see

    appraisals = Appraisal.objects.select_related("real_estate_main__addressCommune","tasadorUser","visadorUser","property_main").all().order_by('timeCreated')
    appraisals_not_assigned = get_appraisals_not_assigned(request,appraisals)
    appraisals_not_accepted = get_appraisals_not_accepted(request,appraisals)
    appraisals_in_appraisal = get_appraisals_in_appraisal(request,appraisals)
    appraisals_in_revision = get_appraisals_in_revision(request,appraisals)
    appraisals_sent = get_appraisals_sent(request,appraisals)
    appraisals_returned = get_appraisals_returned(request,appraisals)

    # Comment class dictionary, to get in javascript the name of the events (big hack alert)

    comment_mp = Comment.__dict__
    comment_dict = {}
    for k, v in comment_mp.items():
        if isinstance(v,type('')) or isinstance(v,type(1)):
            comment_dict[k] = v
    comment_class = json.dumps(comment_dict)

    appraisal_mp = Appraisal.__dict__
    appraisal_dict = {}
    for k, v in appraisal_mp.items():
        if isinstance(v,type('')) or isinstance(v,type(1)):
            appraisal_dict[k] = v
    appraisal_class = json.dumps(appraisal_dict)

    # Get the id's of appraisals to have notifications; then we need just one query

    notifications = request.user.profile.notifications.all()
    notifications_appraisal_ids = notifications.values_list('appraisal_id', flat=True) 

    # Get groups this user is part of, then we just need one query

    groups = request.user.groups.values_list('name',flat=True)

    # Order of this list determines order in html

    appraisals = [
        {'id':'not_assigned', 'appraisals':appraisals_not_assigned, 'title':'Tasaciones por asignar', 'length':len(appraisals_not_assigned), 'groups':['asignador']},
        {'id':'not_accepted', 'appraisals':appraisals_not_accepted, 'title':'Tasaciones por aceptar', 'length':len(appraisals_not_accepted), 'groups':['tasador','asignador']},
        {'id':'in_appraisal', 'appraisals':appraisals_in_appraisal, 'title':'Tasaciones en proceso', 'length':len(appraisals_in_appraisal), 'groups':['tasador','asignador']},
        {'id':'in_revision', 'appraisals':appraisals_in_revision, 'title':'Tasaciones en revisión', 'length':len(appraisals_in_revision), 'groups':['visador','asignador']},
        {'id':'returned', 'appraisals':appraisals_returned, 'title':'Tasaciones devueltas', 'length':len(appraisals_returned),'groups':['visador','asignador']},
        {'id':'sent', 'appraisals':appraisals_sent, 'title':'Tasaciones enviadas', 'length':len(appraisals_sent),'groups':['visador','asignador']}
    ]

    context = {
        'appraisals':appraisals,
        'comment_class':comment_class,
        'appraisal_class':appraisal_class,
        'notifications_appraisal_ids':notifications_appraisal_ids,
        'groups':groups}

    return render(request, 'list/index.html', context)

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

    # Get appraisals that this user can see
    #appraisals_not_assigned, appraisals_active, appraisals_finished = userAppraisals(request)
    appraisals_imported = appraisals_get_imported(request.user)


    context = {
        'evaluationForm': evaluationForm,
        'appraisals_imported': appraisals_imported}

    return render(request, 'list/appraisals_imported.html', context)

def appraisals_get_state(state):
    appraisals = Appraisal.objects.select_related("real_estate_main__addressCommune","tasadorUser","visadorUser").filter(state=state).order_by('timeCreated')
    if state == Appraisal.STATE_NOT_ASSIGNED:
        item = {'id':'not_assigned', 'appraisals':appraisals, 'title':'Tasaciones por asignar', 'length':len(appraisals)}
    elif state == Appraisal.STATE_NOT_ACCEPTED:
        item = {'id':'not_accepted', 'appraisals':appraisals, 'title':'Tasaciones por aceptar', 'length':len(appraisals)}
    elif state == Appraisal.STATE_IN_APPRAISAL:
        item = {'id':'in_appraisal', 'appraisals':appraisals, 'title':'Tasaciones en proceso', 'length':len(appraisals)}
    return item

def render_appraisals_table(request, state):
    item = appraisals_get_state(state)
    notifications = request.user.profile.notifications.all()
    notifications_appraisal_ids = notifications.values_list('appraisal_id', flat=True) 
    return render(request,'list/appraisals_table.html',{'item':item,'table':item["id"],'notifications_appraisal_ids':notifications_appraisal_ids})

def render_appraisals_row(request, table, appraisal):
    return render(request,'list/appraisals_'+table+'_tr.html',{'appraisal':appraisal})

def ajax_archive_appraisal(request):
    '''
    Archive button of finished appraisals. Moves them in to the archive.
    '''
    appraisal = getAppraisalFromRequest(request)
    appraisal.state_last = appraisal.state
    appraisal.state = Appraisal.STATE_ARCHIVED
    appraisal.save()
    return render_appraisals_row(request, 'table_sent', appraisal)

def ajax_comment(request):
    '''
    Make a comment. This is an AJAX request called when the button comment is pressed.
    It should return the list of comments in logbook.html.
    '''
    appraisal_id = int(request.POST['appraisal_id'])

    appraisal = Appraisal.objects.get(id=appraisal_id)
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
    if event == Comment.EVENT_ABORTADO:
        appraisal.state_last = appraisal.state
        appraisal.state = Appraisal.STATE_ABORTED
        #appraisal.in_conflict = True
        appraisal.save()


    comment = appraisal.addComment(int(request.POST['event']),request.user,datetime.datetime.now(timezone_cl),text)

    comments = appraisal.comments.all().order_by('-timeCreated')

    form_comment = FormComment(label_suffix='')
    form_comment.fields['event'].choices = appraisal.getCommentChoices(comments,state=appraisal.state,user=request.user)

    # We need to add notifications to the relevant people. The tasador and visador of the appraisal,
    # and all other higher members like asignadores
    if appraisal.tasadorUser != None:
        if appraisal.tasadorUser != request.user: # dont add notifications to yourself
            appraisal.tasadorUser.profile.addNotification(ntype="comment",appraisal_id=appraisal_id,comment_id=comment.id)
    if appraisal.visadorUser != None:
        if appraisal.visadorUser != request.user: # dont add notifications to yourself
            appraisal.visadorUser.profile.addNotification(ntype="comment",appraisal_id=appraisal_id,comment_id=comment.id)    
    asignadores = User.objects.filter(groups__name='asignador')
    for asignador in asignadores:
        if asignador != request.user: # dont add notifications to yourself
            asignador.profile.addNotification(ntype="comment",appraisal_id=appraisal_id,comment_id=comment.id)

    notifications = request.user.profile.notifications.all()
    notifications_comment_ids = notifications.values_list('comment_id', flat=True) 

    return render(request,'list/comment.html',{'comment':comment,'notifications_comment_ids':notifications_comment_ids})

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
    elif comment.event == Comment.EVENT_INCIDENCIA:
        appraisal.in_conflict = False
        appraisal.save()
    comment.delete()

    form_comment = FormComment(label_suffix='')
    choices = appraisal.getCommentChoices(state=appraisal.state,user=request.user)

    return JsonResponse({'comment_id':comment_id,'choices':choices})

def ajax_validate_cliente(request):
    appraisal_id = int(request.GET['appraisal_id'])
    t = int(request.GET['type'])
    appraisal = Appraisal.objects.get(id=appraisal_id)
    if t == 1:
        if appraisal.clienteValidado:
            appraisal.clienteValidado = False
            comment = appraisal.addComment(Comment.EVENT_CLIENTE_INVALIDADO,request.user,datetime.datetime.now(timezone_cl))
        else:
            appraisal.clienteValidado = True
            comment = appraisal.addComment(Comment.EVENT_CLIENTE_VALIDADO,request.user,datetime.datetime.now(timezone_cl))
    elif t == 2:
        if appraisal.contactoValidado:
            appraisal.contactoValidado = False
            comment = appraisal.addComment(Comment.EVENT_CONTACTO_INVALIDADO,request.user,datetime.datetime.now(timezone_cl))
        else:
            appraisal.contactoValidado = True
            comment = appraisal.addComment(Comment.EVENT_CONTACTO_VALIDADO,request.user,datetime.datetime.now(timezone_cl))
    appraisal.save()
    return render(request,'list/comment.html',{'comment':comment})

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
    print(request.GET)
    appraisal_id = int(request.GET['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)

    table = request.GET['table']

    groups = request.user.groups.values_list('name',flat=True)
    
    return render(request,'list/appraisals_'+table+'_tr.html',{'appraisal':appraisal,'groups':groups})

def ajax_evaluate_modal(request):
    '''
    Called when opening the logbook modal, through AJAX. Returns the comments of the relevant appraisal.
    '''
    appraisal_id = int(request.GET['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)

    try:
        evaluationForm = EvaluationForm(instance=appraisal.appraisalevaluation)
    except:
        appraisal_evaluation = AppraisalEvaluation(user=appraisal.tasadorUser,appraisal=appraisal)
        appraisal_evaluation.save()
        appraisal.save()
        evaluationForm = EvaluationForm(instance=appraisal_evaluation)

    return render(request,'list/modals/modal_evaluate.html',{'appraisal':appraisal,'evaluationForm':evaluationForm})

def ajax_evaluate_modal_close(request):
    '''
    Called when opening the logbook modal, through AJAX. Returns the comments of the relevant appraisal.
    '''
    appraisal_id = int(request.POST['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)
    evaluationForm = EvaluationForm(request.POST,instance=appraisal.appraisalevaluation)
    evaluationForm.save()
    appraisal.save()

    groups = request.user.groups.values_list('name',flat=True)

    return render(request,'list/appraisals_table_sent_tr.html',{'appraisal':appraisal,'groups':groups})

def ajax_mark_as_returned(request):
    '''
    '''
    appraisal_id = int(request.POST['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)
    comment = appraisal.addComment(Comment.EVENT_RETURNED,request.user,datetime.datetime.now(timezone_cl))
    if datetime.datetime.now(timezone_cl).hour >= 12:
        tomorrow = datetime.datetime.now(tz=timezone_cl).replace(minute=00, hour=12, second=00, microsecond=0) + datetime.timedelta(days=1)
        appraisal.timeDue = tomorrow
    else:
        today = datetime.datetime.now(timezone_cl).replace(minute=59, hour=23, second=59,microsecond=0)
        appraisal.timeDue = today

    appraisal.state = Appraisal.STATE_RETURNED
    appraisal.save()
    if appraisal.visadorUser:
        appraisal.visadorUser.profile.addNotification("comment",appraisal_id,comment.id)

    return JsonResponse({})

def ajax_solve_conflict(request):
    
    appraisal_id = int(request.GET['appraisal_id'])
    table = request.GET['table']

    appraisal = Appraisal.objects.get(id=appraisal_id)
    appraisal.in_conflict = False;
    appraisal.save()

    groups = request.user.groups.values_list('name',flat=True)

    return render(request,'list/appraisals_'+table+'_tr.html',{'appraisal':appraisal,'groups':groups})

def ajax_upload_report(request):

    appraisal_id = int(request.POST['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)

    for report_file in request.FILES.getlist('report'):
        report = Report(report=report_file,appraisal=appraisal,time_uploaded=datetime.datetime.now(timezone_cl))
        report.save()
        appraisal.save()

    comment = appraisal.addComment(Comment.EVENT_REPORTE_ADJUNTO,request.user,datetime.datetime.now(timezone_cl))

    #notifications = request.user.user.notifications.all()
    #notifications_comment_ids = notifications.values_list('comment_id', flat=True) 

    ##return render(request,'list/comment.html',{'comment':comment,'notifications_comment_ids':notifications_comment_ids})

    comments = appraisal.comments.select_related('user').all().order_by('-timeCreated')
    form_comment = FormComment(label_suffix='')
    
    form_comment.fields['event'].choices = appraisal.getCommentChoices(comments,state=appraisal.state,user=request.user)

    notifications = request.user.profile.notifications.all()
    notifications_comment_ids = notifications.values_list('comment_id', flat=True) 

    groups = request.user.groups.values_list('name',flat=True)

    reports = appraisal.report_set.order_by('time_uploaded')

    return render(request,'logbook/modals_logbook.html',
        {'appraisal':appraisal,
        'comments':comments,
        'form_comment':form_comment,
        'groups':groups,
        'reports': reports,
        'notifications_comment_ids':notifications_comment_ids})

def ajax_save_time_due(request):
    appraisal_id = int(request.GET['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)
    appraisal.timeDue = datetime.datetime.strptime(request.GET['datetime'],'%d/%m/%Y %H:%M')
    appraisal.save()
    return JsonResponse({'datetime':request.GET['datetime']})

def load_communes(request):
    region_id = int(request.GET.get('region'))
    region = Region.objects.get(pk=region_id)
    communes = list(Commune.objects.filter(region=region.code).order_by('name'))
    return render(request,
        'hr/commune_dropdown_list_options.html',
        {'communes': communes})


def ajax_expenses_modal(request):
    '''
    Called when opening the expenses modal, through AJAX. Returns the comments of the relevant appraisal.
    '''
    appraisal_id = int(request.GET['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)
    expenses = AppraiserExpenses.objects.filter(appraisal=appraisal)
    form_expenses = FormExpenses(label_suffix='')
    groups = request.user.groups.values_list('name', flat=True)

    return render(request, 'list/modals/modal_expenses.html',
                  {'appraisal': appraisal,
                   'expenses': expenses,
                   'form_expenses': form_expenses,
                   'groups': groups})

def ajax_save_expenses(request):
    '''
    save expenses from modal
    '''

    appraisal_id = int(request.POST['appraisal_id'])
    description = request.POST['description']
    totalPrice = int(request.POST['totalPrice'])
    appraisal = Appraisal.objects.get(id=appraisal_id)
    expense = AppraiserExpenses(appraisal=appraisal, description=description, totalPrice=totalPrice)
    expense.save()

    return render(request, 'list/expenses.html',
                  {'appraisal': appraisal,
                   'expense': expense})

def ajax_delete_expenses(request):
    '''
    deletes expenses from modal
    '''
    appraisal_id = int(request.POST['appraisal_id'])
    expense_id = int(request.POST['expense_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)
    expense = AppraiserExpenses(appraisal=appraisal, id=expense_id)
    expense.delete()
    print(request.POST)

    return render(request, 'list/expenses.html',
                  {'appraisal': appraisal,
                   'expense': expense})