from django.urls import path
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    ]
