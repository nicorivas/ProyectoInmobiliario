from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from appraisal.models import Appraisal
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned


class appraiserListOfAppraisals(LoginRequiredMixin, ListView):
    """
        Generic class-based view listing appraisals on loan to current user.
        """
    model = Appraisal
    template_name = 'user/index.html'
    paginate_by = 10

    def get_queryset(self):
        return Appraisal.objects.filter(tasadorUser=self.request.user).filter(status=Appraisal.STATE_ACTIVE).order_by('timeCreated')


@login_required(login_url='/')
def userAppraisals(request):

    appraisals_active = Appraisal.objects.filter(status=Appraisal.STATE_ACTIVE).order_by('timeCreated')

    appraisals_finished = Appraisal.objects.filter(status=Appraisal.STATE_FINISHED).order_by('timeCreated')

    context = {
        'appraisals_active': appraisals_active,
        'appraisals_finished': appraisals_finished}
    return render(request, 'user/index.html', context)


