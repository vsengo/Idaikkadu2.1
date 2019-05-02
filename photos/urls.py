from django.conf.urls import url

from . import views

app_name = 'photos'

urlpatterns = [
    url(r'^clear/$', views.clear_database, name='clear_database'),
    url(r'^upload-photos$', views.UploadPhotosView.as_view(), name='upload-photos'),
    url(r'^view-photos$', views.PhotoList.as_view(), name='view-photos')
]
