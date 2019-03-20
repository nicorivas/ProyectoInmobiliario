from django.views.generic import FormView
from django.shortcuts import render
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q

from appraisal.models import Appraisal
from .forms import FormSearch

@login_required(login_url='/user/login')
def archive(request):
	
	form_search = FormSearch(label_suffix="")

	appraisals = Appraisal.objects.select_related("real_estate_main__addressCommune","tasadorUser","visadorUser","property_main").all().order_by('-timeCreated')

	context = {'form_search':form_search,'appraisals':appraisals}

	return render(request, 'archive/archive.html', context)

def ajax_unarchive_appraisal_modal(request):
	appraisal_id = int(request.GET['appraisal_id'])
	appraisal = Appraisal.objects.get(id=appraisal_id)
	context = {'appraisal':appraisal}
	return render(request, 'archive/modals_unarchive.html', context)

def ajax_unarchive_appraisal(request):
	appraisal_id = int(request.GET['appraisal_id'])
	appraisal = Appraisal.objects.get(id=appraisal_id)
	s = appraisal.state
	appraisal.state = appraisal.state_last
	appraisal.state_last = s
	appraisal.save()
	context = {'appraisal':appraisal}
	return render(request, 'archive/appraisals_search_tr.html', context)

def ajax_delete_appraisal_modal(request):
	appraisal_id = int(request.GET['appraisal_id'])
	appraisal = Appraisal.objects.get(id=appraisal_id)
	context = {'appraisal':appraisal}
	return render(request, 'archive/modals_delete.html', context)

def ajax_delete_appraisal(request):
	appraisal_id = int(request.GET['appraisal_id'])
	appraisal = Appraisal.objects.get(id=appraisal_id)
	appraisal.delete()
	context = {'appraisal':appraisal}
	return render(request, 'archive/appraisals_search_tr.html', context)

def ajax_search(request):

	appraisals = Appraisal.objects.select_related("real_estate_main__addressCommune","tasadorUser","visadorUser","property_main").all().order_by('timeCreated')

	if request.POST['state'] != '':
		appraisals = appraisals.filter(state=request.POST['state'])
	if request.POST['code'] != '':
		appraisals = appraisals.filter(id__iexact=request.POST['code'])
	if request.POST['solicitante'] != '':
		appraisals = appraisals.filter(solicitante=request.POST['solicitante'])
	if request.POST['solicitanteCodigo'] != '':
		appraisals = appraisals.filter(solicitanteCodigo__iexact=request.POST['solicitanteCodigo'])
	if request.POST['addressStreet'] != '':
		appraisals = appraisals.filter(real_estates__addressStreet__icontains=request.POST['addressStreet'])
	if request.POST['addressNumber'] != '':
		appraisals = appraisals.filter(real_estates__addressNumber__icontains=request.POST['addressNumber'])
	if request.POST['addressCommune'] != '':
		appraisals = appraisals.filter(real_estates__addressCommune__id=int(request.POST['addressCommune']))
	print(request.POST)
	if request.POST['addressRegion'] != '':
		appraisals = appraisals.filter(real_estates__addressRegion__id=int(request.POST['addressRegion']))
	if request.POST['tasador'] != '':
		appraisals = appraisals.filter(Q(tasadorUser__first_name__icontains=request.POST['tasador'])|\
							   		   Q(tasadorUser__last_name__icontains=request.POST['tasador']))
	if request.POST['visador'] != '':
		appraisals = appraisals.filter(Q(visadorUser__first_name__icontains=request.POST['visador'])|\
									   Q(visadorUser__last_name__icontains=request.POST['visador']))
	if request.POST['timeCreatedFrom'] != '':
		appraisals = appraisals.filter(timeCreated__gte=request.POST['timeCreatedFrom'])
	if request.POST['timeCreatedUntil'] != '':
		appraisals = appraisals.filter(timeCreated__lte=request.POST['timeCreatedUntil'])
	if request.POST['timeFinishedFrom'] != '':
		appraisals = appraisals.filter(timeFinished__gte=request.POST['timeFinishedFrom'])
	if request.POST['timeFinishedUntil'] != '':
		appraisals = appraisals.filter(timeFinished__lte=request.POST['timeFinishedUntil'])


	context = {'appraisals':appraisals}

	return render(request, 'archive/appraisals_search.html', context)	