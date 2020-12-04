from django.conf.urls import url

from . import views

app_name = 'photos'

urlpatterns = [
    url(r'^add-album', views.AddAlbum, name='add-album'),
    url(r'^view-album/(?P<album_id>\d+)', views.ViewAlbum, name='view-album')
]
