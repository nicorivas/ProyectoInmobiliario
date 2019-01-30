"""map URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from home.forms import AuthenticationFormB
from django.views.generic import RedirectView

from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar

urlpatterns = [
    path('viz/', include('viz.urls')),
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('main/', include('main.urls')),
    path('realestate/', include('realestate.urls')),
    path('create/', include('create.urls')),
    path('appraisal/', include('appraisal.urls')),
    path('accounting/', include('accounting.urls')),
    path('region/', include('region.urls')),
    path('province/', include('province.urls')),
    path('commune/', include('commune.urls')),
    path('square/', include('square.urls')),
    path('user/', include('user.urls')),
    path('vis/', include('vis.urls')),
    path('evaluation/', include('evaluation.urls')),
    path('archive/', include('archive.urls')),
    #path('', auth_views.LoginView.as_view(redirect_field_name='user:tasaciones', template_name='user/login.html',
    #    form_class=AuthenticationFormB), name='login'),
    path('logout/', auth_views.LogoutView.as_view(redirect_field_name='home')),
    path('__debug__/', include(debug_toolbar.urls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
