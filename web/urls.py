from django.urls import path

from . import views

app_name = 'web'

urlpatterns = [
    path(r'create', views.add_news, name='news_create'),
    path(r'save', views.add_news, name='news_save'),
    ]
