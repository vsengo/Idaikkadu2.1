from django.urls import path

from . import views

app_name = 'web'

urlpatterns = [
    path('', views.index, name='index'),
    path('news/create/', views.add_news, name='news_create'),
    path('news/save/', views.add_news, name='news_save'),
    ]
