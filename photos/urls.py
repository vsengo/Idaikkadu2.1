from django.conf.urls import url

from . import views

app_name = 'photos'

urlpatterns = [
    url(r'^clear', views.clear_database, name='clear_database'),
    url(r'^upload-photos', views.upload_photos2, name='upload-photos'),
    url(r'^add-photos', views.UploadPhotosView.as_view(), name='upload_photos2'),
    url(r'^view-photos', views.PhotoList.as_view(), name='view-photos')
]
