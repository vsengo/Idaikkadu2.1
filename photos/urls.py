from django.conf.urls import url

from . import views
app_name='photos'

urlpatterns = [
    url(r'^get_description/$', views.get_description, name='get_description'),
    url(r'^add_to_album/$', views.add_to_album, name='add_to_album'),
    url(r'^photo_form$', views.load_photoform, name='load_photo_form'),
    url(r'^save/$', views.AlbumView.as_view(), name='album_form_save'),
    url(r'^close_photos$', views.AlbumView.as_view(), name='close_photos'),
    url(r'^progress-bar-upload/$', views.ProgressBarUploadView.as_view(), name='progress_bar_upload'),
]