from django.conf.urls import url

from . import views
app_name='photos'

urlpatterns = [
    url(r'^get_description/$', views.get_description, name='get_description'),
    url(r'^photo_form$', views.PhotoView.as_view(), name='photo_form'),
    url(r'^save_photos$', views.PhotoView.as_view(), name='photo_form'),
    url(r'^save/', views.AlbumView.as_view(), name='photo_form_save'),
    url(r'^close_photos$', views.AlbumView.as_view(), name='close_photos'),
]