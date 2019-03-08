from django.views.generic import FormView
from django.shortcuts import render, redirect

from appraisal.models import Appraisal
from django.contrib.auth.forms import AuthenticationForm
from .forms import AuthenticationFormB
from django.contrib.auth import authenticate, login

def home(request):

	# If user is logged in, the main page is the list of appraisals.
	if request.user.is_authenticated:
		return redirect('list/')

	# Otherwise show the nice intro page

	# This comes from the login form:
	login_error = False
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
				return redirect('list/')
		else:
			context = {'form_login':form_login}
			return render(request, 'home/index.html', context)

	form_login = AuthenticationFormB()
	context = {'form_login':form_login,'error':login_error}
	return render(request, 'home/index.html', context)
