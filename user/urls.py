from django.urls import path

from . import views

urlpatterns = [
    path('register', views.register),
    path('login', views.login),
    path('check_login', views.check_login),
    path('logout', views.logout),
]
