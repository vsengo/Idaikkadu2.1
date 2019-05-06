from django.conf.urls import url
from . import views

app_name = 'news'

urlpatterns = [
    url(r'^view-news$', views.NewsList.as_view(), name='news_list'),
    url(r'^add-news$', views.AddNewsView.as_view(), name='add-news'),
    url(r'(?P<pk>\d+)/$', views.DetailNewsView.as_view(), name='detail-news'),
    url(r'^jaffna-news$', views.JaffnaNewsView.as_view(), name='jaffna-news'),
    url(r'^srilanka-news$', views.SrilankaNewsView.as_view(), name='srilanka-news'),
    url(r'^international-news$', views.InternationalNewsView.as_view(), name='international-news'),
]
