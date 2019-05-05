from django.conf.urls import url
from . import views

app_name = 'news'

urlpatterns = [
    url(r'^view-news$', views.NewsList.as_view(), name='news_list'),
    url(r'^add-news$', views.AddNewsView.as_view(), name='add-news'),
    url(r'(?P<pk>\d+)/$', views.DetailNewsView.as_view(), name='detail-news')
]
