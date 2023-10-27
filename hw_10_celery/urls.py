"""
URL configuration for hw_10_celery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path

from sms.views import verification, authentication, send_an_sms, index, verification_success, authentication_error

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('verification/', verification, name='verification'),
    path('authentication/', authentication, name='authentication'),
    path('send_sms/', send_an_sms, name='send_an_sms'),
    path('verification_success/', verification_success, name='verification_success'),
    path('authentication_error/', authentication_error, name='authentication_error'),

]
