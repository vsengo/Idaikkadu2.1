from django.conf.urls import url

from . import views

app_name = 'photos'

urlpatterns = [
    url(r'^add-album', views.AddAlbum, name='add-album'),
    url(r'^view-album/(?P<album_id>\d+)', views.ViewAlbum, name='view-album'),
    url(r'^all-album', views.ShowAllAlbum, name='all-album'),
    url(r'^update-album', views.UpdateAlbum, name='update-album'),
    url(r'^approve-album/(?P<album_id>\d+)', views.ApproveAlbum, name='approve-album'),
    url(r'^delete-album/(?P<album_id>\d+)', views.DeleteAlbum, name='delete-album'),
    url(r'^comment-album/(?P<pk>\d+)', views.PostComment, name='comment-album'),
    url(r'^like-album/(?P<pk>\d+)', views.LikeAlbum, name='like-album'),
]
