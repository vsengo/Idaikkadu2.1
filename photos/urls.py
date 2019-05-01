from django.conf.urls import url

from . import views

app_name = 'photos'

urlpatterns = [
    url(r'^clear/$', views.clear_database, name='clear_database'),
    url(r'^upload-photos$', views.upload_photos.as_view(), name='progress_bar_upload'),
]
