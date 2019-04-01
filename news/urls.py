from django.conf.urls import url

from . import views
app_name = 'news'

urlpatterns = [
    url(r'^add-news$', views.create, name='add-news'),
 ]