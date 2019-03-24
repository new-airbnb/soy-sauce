from django.urls import path

from . import views

urlpatterns = [
    path('create', views.create),
    path('upload_photo', views.upload_photo),
    path('search', views.search),
    path('info', views.info),
    path('create_booking', views.create_booking),
    path('download_photos', views.download_photos),
    path('create_comment', views.create_comment),
    path('get_comments', views.get_comments)
]
