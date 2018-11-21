from django.views.generic import FormView
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from appraisal.models import Appraisal
from django.contrib.auth.forms import AuthenticationForm
from .forms import AuthenticationFormB
from django.contrib.auth import authenticate, login

def home(request):

	if request.user.is_authenticated:
		return redirect('main/')

	if request.method == 'POST':
		# Login
		form_login = AuthenticationFormB(data=request.POST)
		if form_login.is_valid():
			print(form_login.cleaned_data['username'],form_login.cleaned_data['password'])
			user = authenticate(
				username=form_login.cleaned_data['username'],
				password=form_login.cleaned_data['password'])
			if user is not None:
				login(request, user)
				return HttpResponseRedirect('main/')
		else:
			print(form_login.errors)

	form_login = AuthenticationFormB()
	context = {'form_login':form_login}

	return render(request, 'home/index.html', context)
