from django.conf.urls import url

from . import views

app_name = 'photos'

urlpatterns = [
    url(r'^add-album', views.AddAlbum, name='add-album'),
    url(r'^view-photos', views.PhotoList.as_view(), name='view-photos')
]
