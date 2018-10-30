from django.views.generic import FormView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from user.views import userAppraisals
from appraisal.models import Appraisal

@login_required(login_url='/user/login')
def main(request):

    if request.method == 'POST':
        if 'delete' in request.POST:
            # Handle the delete button, next to every appraisal
            id = int(request.POST['appraisal_id'])
            appraisal = Appraisal.objects.get(pk=id)
            appraisal.delete()

    appraisals_active, appraisals_finished = userAppraisals(request)

    context = {
        'appraisals_active': appraisals_active,
        'appraisals_finished': appraisals_finished}

    return render(request, 'main/index.html', context)
