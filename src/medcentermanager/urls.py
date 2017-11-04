"""medcentermanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import (url, include)
from django.contrib import admin

from users.views import (RegistrationView, LoginView, LogoutView)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^dashboard/', include('dashboard.urls', namespace='dashboard')),
    url(r'^users/', include('users.urls', namespace='users')),
    
    url(r'^registration/(?P<user_type>\w+)', RegistrationView.as_view(), name='registration'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout')
]
