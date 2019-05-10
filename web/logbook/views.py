import json
from appraisal.models import Appraisal, Comment
from appraisal.forms import FormComment
from django.http import HttpResponse
from django.shortcuts import render

def main(request):
    return HttpResponse('')

def ajax_logbook(request):
    '''
    Called when opening the logbook modal, through AJAX. Returns the comments of the relevant appraisal.
    '''
    appraisal_id = int(request.GET['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)
    comments = appraisal.comments.select_related('user').all().order_by('-timeCreated')
    form_comment = FormComment(label_suffix='')

    form_comment.fields['event'].choices = appraisal.getCommentChoices(comments,state=appraisal.state,user=request.user)

    notifications = request.user.profile.notifications.all()
    notifications_comment_ids = notifications.values_list('comment_id', flat=True) 

    groups = request.user.groups.values_list('name',flat=True)

    reports = appraisal.report_set.order_by('time_uploaded')

    comment_mp = Comment.__dict__
    comment_dict = {}
    for k, v in comment_mp.items():
        if isinstance(v,type('')) or isinstance(v,type(1)):
            comment_dict[k] = v
    comment_class = json.dumps(comment_dict)

    return render(request,'logbook/modals_logbook.html',
        {'appraisal':appraisal,
        'comments':comments,
        'form_comment':form_comment,
        'groups':groups,
        'reports':reports,
        'comment_class':comment_class,
        'notifications_comment_ids':notifications_comment_ids})

def ajax_logbook_close(request):
    '''
    Called when closing the logbook modal, through AJAX.
    1. Deletes notifications.
    2. Saves modified variables
    '''
    appraisal_id = int(request.POST['appraisal_id'])
    request.user.profile.removeNotification(ntype="comment",appraisal_id=appraisal_id)

    appraisal = Appraisal.objects.get(id=appraisal_id)

    if request.POST['valorUF'] in ["None",""]:
        appraisal.valorUF = None
    else:
        appraisal.valorUF = request.POST['valorUF']

    if request.POST['solicitanteEjecutivo'] in ["None",""]:
        appraisal.solicitanteEjecutivo = None
    else:
        appraisal.solicitanteEjecutivo = request.POST['solicitanteEjecutivo']
    if request.POST['solicitanteEjecutivoEmail'] in ["None",""]:
        appraisal.solicitanteEjecutivoEmail = None
    else:
        appraisal.solicitanteEjecutivoEmail = request.POST['solicitanteEjecutivoEmail']
    if request.POST['solicitanteEjecutivoTelefono'] in ["None",""]:
        appraisal.solicitanteEjecutivoTelefono = None
    else:
        appraisal.solicitanteEjecutivoTelefono = request.POST['solicitanteEjecutivoTelefono']

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