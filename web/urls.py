from django.urls import path, include
from django.conf.urls import url
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    ]
