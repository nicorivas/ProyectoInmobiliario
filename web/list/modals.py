from appraisal.models import Appraisal, Comment, Report, AppraiserExpenses
from django.shortcuts import render
from commune.models import Commune
from region.models import Region
from django.http import HttpResponse, JsonResponse
from . import views
from user.views import appraiserWork, visadorWork
from django.contrib.auth.models import User
from .forms import TasadorSearch
import datetime
import pytz

timezone_cl = pytz.timezone('Chile/Continental')

def ajax_assign_tasador_modal(request):
    '''
    Assign a tasador from an appraisal. Gets called through AJAX when clicked
    on the corresponding modal, which has a form where you can select the user.
    '''
    appraisal = Appraisal.objects.get(id=int(request.GET['appraisal_id']))
    return render(request,'list/modals/modal_assign_tasador.html',{'appraisal':appraisal})

def ajax_assign_tasador_tasadores(request):
    tasadores = User.objects.filter(groups__name__in=['tasador']).order_by('last_name')
    tasadores_info = appraiserWork(tasadores)
    regions = Region.objects.only('name').order_by('code')
    communes = Commune.objects.only('name').order_by('name')
    form = TasadorSearch(label_suffix='')
    form.fields['addressRegion'].queryset = regions
    form.fields['addressCommune'].queryset = communes
    return render(request,'list/modals/modal_assign_tasador_tasadores.html',{'tasadores':tasadores_info,'form':form})

def ajax_assign_tasador(request):
    '''
    Assign a tasador from an appraisal. Gets called through AJAX when clicked
    on the corresponding modal, which has a form where you can select the user.
        1. Assign tasador to appraisal
        2. Add the event, with a default text + any other comment added.
        3. Add notification to the new tasador.
        4. Add notification to visador, if it exists.
        5. Change the state of the appraisal
        @: Return list of not accepted appraisals to replace table.
    '''
    appraisal_id = int(request.POST['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)

    if 'tasador' not in request.POST:
        response = JsonResponse({'alert':"Debe seleccionar un tasador"})
        response.status_code = 403
        return response

    tasador_id = int(request.POST['tasador'])
    tasador = User.objects.get(id=tasador_id)
    user = request.user

    # 1
    appraisal.tasadorUser = tasador
    # 2
    comment = appraisal.addComment(Comment.EVENT_TASADOR_SOLICITADO,user,datetime.datetime.now(timezone_cl),
        text="Tasación solicitada a "+tasador.first_name +' '+ tasador.last_name)
    # 3
    appraisal.tasadorUser.profile.addNotification(ntype="comment",appraisal_id=appraisal_id,comment_id=comment.id)
    if appraisal.visadorUser:
        appraisal.visadorUser.profile.addNotification(ntype="comment",appraisal_id=appraisal_id,comment_id=comment.id)
    # 4
    appraisal.state = Appraisal.STATE_NOT_ACCEPTED
    appraisal.save()

    notifications = request.user.profile.notifications.all()
    notifications_appraisal_ids = notifications.values_list('appraisal_id', flat=True) 

    item = views.appraisals_get_state(Appraisal.STATE_NOT_ACCEPTED)
    
    return render(request,'list/appraisals_table.html',{'item':item,'table':item["id"]})

    #appraisals_not_accepted = views.appraisals_get_state(Appraisal.STATE_NOT_ACCEPTED)
    #
    #return render(request,'list/appraisals_table_not_accepted.html',
    #    {'appraisals_not_accepted':appraisals_not_accepted,
    #     'notifications_appraisal_ids':notifications_appraisal_ids})

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
    appraisal.addComment(Comment.EVENT_TASADOR_DESASIGNADO,user,datetime.datetime.now(timezone_cl),
        text="Tasador "+tasador.first_name+" "+tasador.last_name+" fue desasignado.")
    appraisal.save()

    notifications = request.user.profile.notifications.all()
    notifications_appraisal_ids = notifications.values_list('appraisal_id', flat=True) 

    item = views.appraisals_get_state(Appraisal.STATE_NOT_ASSIGNED)
    
    return render(request,'list/appraisals_table.html',{'item':item,'table':item["id"]})

    #return render(request,'list/appraisals_table_not_assigned.html',
    #    {'appraisals_not_assigned':appraisals_not_assigned,
    #     'notifications_appraisal_ids':notifications_appraisal_ids})

#------------------------------------------------------------------------------------------------

def ajax_assign_visador_modal(request):
    '''
    Assign a visador from an appraisal. Gets called through AJAX when clicked
    on the corresponding modal, which has a form where you can select the user.
    '''
    appraisal = Appraisal.objects.get(id=int(request.GET['appraisal_id']))
    return render(request,'list/modals/modal_assign_visador.html',{'appraisal':appraisal})

def ajax_assign_visador(request):
    '''
    Assign a visador from an appraisal. Gets called through AJAX when clicked
    on the corresponding modal, which has a form where you can select the user.
    Button can be called from two tables, so different appraisals must be get
    to modify the correct one.
    '''
    appraisal_id = int(request.POST['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)
    visador_id = int(request.POST['visador'])
    visador = User.objects.get(id=visador_id)
    user_id = int(request.user.id)
    user = User.objects.get(id=user_id)

    status = ""
    if appraisal.visadorUser == visador:
        status = "Visador ya seleccionado"
    else:
        appraisal.visadorUser = visador
        comment = appraisal.addComment(Comment.EVENT_VISADOR_ASIGNADO,user,datetime.datetime.now(timezone_cl),
            text="Visación asignada a "+visador.first_name+' '+visador.last_name)
        appraisal.visadorUser.profile.addNotification("comment",appraisal_id,comment.id)
        appraisal.save()

    notifications = request.user.profile.notifications.all()
    notifications_appraisal_ids = notifications.values_list('appraisal_id', flat=True) 

    if request.POST['parent'] == 'table_not_assigned':
        item = views.appraisals_get_state(Appraisal.STATE_NOT_ASSIGNED)
    elif request.POST['parent'] == 'table_in_appraisal':
        item = views.appraisals_get_state(Appraisal.STATE_IN_APPRAISAL)
    
    return render(request,'list/appraisals_table.html',{'item':item,'table':item["id"]})

def ajax_assign_visador_visadores(request):
    '''
    Load list of visadores
    '''
    appraisal_id = int(request.GET['appraisal_id'])
    appraisal = Appraisal.objects.get(id=appraisal_id)
    if appraisal.visadorUser:
        visador_current = appraisal.visadorUser.id
    else:
        visador_current = None

    visadores = User.objects.filter(groups__name__in=['visador']).order_by('last_name')
    visadores_info = visadorWork(visadores)
    regions = Region.objects.only('name').order_by('code')
    communes = Commune.objects.only('name').order_by('name')
    form = TasadorSearch(label_suffix='')
    form.fields['addressRegion'].queryset = regions
    form.fields['addressCommune'].queryset = communes
    return render(request,'list/modals/modal_assign_visador_visadores.html',{'visadores':visadores_info,'visador_current':visador_current,'form':form})

def ajax_unassign_visador(request):
    '''
    Unassign a tasador from an appraisal. Gets called through AJAX when clicked
    on the corresponding confirmation modal.
    '''
    appraisal_id = int(request.GET['appraisal_id'])
    table_id = request.GET['parent']
    appraisal = Appraisal.objects.get(id=appraisal_id)
    visador = appraisal.visadorUser
    if visador != None:
        comment = appraisal.addComment(Comment.EVENT_VISADOR_DESASIGNADO,request.user,datetime.datetime.now(timezone_cl),
            text="Visador "+visador.first_name+' '+visador.last_name+" fue desasignado.")
        appraisal.visadorUser.profile.addNotification("comment",appraisal_id,comment.id)
        appraisal.visadorUser = None
        appraisal.save()
    else:
        response = JsonResponse({'alert':"Debe seleccionar un tasador"})
        response.status_code = 403
        return response

    return render(request,'list/appraisals_'+table_id+'_tr.html',{'appraisal':appraisal})