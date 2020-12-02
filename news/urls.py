from django.conf.urls import url
from django.urls import path
from django.contrib.auth.decorators import permission_required

from news.views import AddNewsView
from . import views

app_name = 'news'

urlpatterns = [
    url(r'^add-news', permission_required('user.view_add_delete')(AddNewsView.as_view()), name='add-news'),
    url(r'^view-news', views.NewsList.as_view(), name='news_list'),
    url(r'^detail-news/(?P<pk>\d)', views.DetailNewsView.as_view(), name='detail-news'),
    url(r'^idaikkadu-news', views.JaffnaNewsView.as_view(), name='idaikkadu-news'),
    url(r'^srilanka-news', views.SrilankaNewsView.as_view(), name='srilanka-news'),
    url(r'^international-news', views.InternationalNewsView.as_view(), name='international-news'),
    url(r'^(?P<pk>\d+)/edit-news', views.NewsUpdate.as_view(), name='edit-news'),
    url(r'^(?P<pk>\d+)/delete-news', views.NewsDelete.as_view(), name='delete-news'),
]
