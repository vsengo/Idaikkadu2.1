from django.conf.urls import url
from . import views

app_name = 'news'

urlpatterns = [
    url(r'^add-news$', views.AddNewsView.as_view(), name='add-news')
]
