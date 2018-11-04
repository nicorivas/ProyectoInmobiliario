from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from home.forms import AuthenticationFormB
from django.conf.urls import url
from django.views.generic import RedirectView
app_name = 'user'

urlpatterns = [
    path('ajax/load-communes/', views.load_communes, name='user_ajax_load_communes'),
    path('', RedirectView.as_view(pattern_name='user:appraisals'), name='user'),
    path('profile/', views.view_profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='profile_edit'),
    path('login/', views.login, name='login'),
    path('tasaciones/', views.userAppraisals, name='appraisals'),
    #path('login/', auth_views.LoginView.as_view(redirect_field_name='user:tasasciones-usuario',
     #       form_class=AuthenticationFormB, template_name='user/login.html'), name='login'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='user/password_reset_form.html',
        email_template_name='user/password_reset_email.html', success_url=reverse_lazy('user:password_reset_done')),
         name='password_reset'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html',
        success_url=reverse_lazy('user:password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'),
        name='password_reset_done'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'),
        name='password_reset_complete'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='user/password_change.html',
            success_url=reverse_lazy('user:password_change_done')), name='password_change'),
    path('password_change/done', auth_views.PasswordChangeDoneView.as_view(template_name='user/password_change_done.html'),
         name='password_change_done'),
    path('profile/evaluation/', views.appraiserEvaluationView, name='apprariserEvaluation')

]