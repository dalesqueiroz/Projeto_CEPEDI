"""
URL configuration for capne project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path, include
#A baixo está sendo acessado a classe RedirectView que é padrão do django
#que tem funções para redirecionar um url para outro
from django.views.generic.base import RedirectView

urlpatterns = [
    # Isso serve para redirecionar a url "" para onde está o login, sendo de forma permanente,
    path('', RedirectView.as_view(url="estudante/login/")),
    path('admin/', admin.site.urls),
    path('estudante/', include('estudante.urls'))
]
