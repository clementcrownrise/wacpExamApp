"""
URL configuration for examLetter project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm


#app_name ='examletter'


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path('signup/', views.signup, name='signup'),
    #path('login/', auth_views.LoginView.as_view(authentication_form=LoginForm,template_name='examLetter/login.html')),
    path('accounts/login/', auth_views.LoginView.as_view(authentication_form=LoginForm,template_name='examLetter/login.html')),
    path('logout/', views.logout_view, name='logout'),  
    path("examination/", include("examination.urls")),
    path("letter/", include("letter.urls")),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
