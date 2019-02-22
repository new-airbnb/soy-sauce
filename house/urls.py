from django.urls import path

from . import views

urlpatterns = [
    path('create', views.create),
    path('upload_photo', views.upload_photo)
]

