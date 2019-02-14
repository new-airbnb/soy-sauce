"""soy_sauce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

urlpatterns = [
    path('', include('website.urls')),
    path('user/', include('user.urls')),
    path('admin/', admin.site.urls)
]

from utils import error_msg
from utils.error_handler import handler
handler400 = lambda req, *args, **kwargs: handler(400, error_msg.MSG_400, kwargs)
handler403 = lambda req, *args, **kwargs: handler(403, error_msg.MSG_403, kwargs)
handler404 = lambda req, *args, **kwargs: handler(404, error_msg.MSG_404, kwargs)
handler500 = lambda req, *args, **kwargs: handler(500, error_msg.MSG_500, kwargs)
