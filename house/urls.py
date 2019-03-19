from django.urls import path

from . import views

urlpatterns = [
    path('create', views.create),
    path('upload_photo', views.upload_photo),
    path('search', views.search),
    path('info', views.info),
    path('create_booking', views.create_booking),
    path('download_photos', views.download_photos)
]
