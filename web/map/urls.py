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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('realestate/', include('realestate.urls')),
    path('create/', include('create.urls')),
    path('appraisal/', include('appraisal.urls')),
    path('region/', include('region.urls')),
    path('province/', include('province.urls')),
    path('commune/', include('commune.urls')),
    path('square/', include('square.urls')),
    path('main/', include('main.urls')),
    #path('', include('home.urls')),
    path('', auth_views.LoginView.as_view(redirect_field_name='main',form_class=AuthenticationFormB)),
    path('logout/', auth_views.LogoutView.as_view(redirect_field_name='home')),
]
